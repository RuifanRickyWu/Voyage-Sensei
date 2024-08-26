import json, os, re, pickle
from tqdm import tqdm

from CarTravel.LLM.GPTChatCompletion import *
from CarTravel.Entity.query import *
from CarTravel.Entity.aspect import *

ANSWER_FORMAT = """{{"answer": {answer}}}"""

class queryProcessor:

    def __init__(self, input_path: str, llm: LLM, output_dir: str = "output"):
        """
        Initialize the query processor
        :param query:
        :param llm:
        :param mode_name: can only be "expand", "reformulate", "elaborate"
        :param output_dir:
        """ 
        self.llm = llm
        self.output_dir = output_dir
        self.query_list = self._load_queries(input_path)
    
    def process_queries(self) -> list[Query]:
        """
        Process the queries
        """
        # # fetch aspect processing function
        # aspect_processing_func = None
        # if self.mode_name == "reformulate":
        #     aspect_processing_func = self._reformulate_aspect
        # elif self.mode_name == "expand":
        #     aspect_processing_func = self._expand_aspect
        # elif self.mode_name == "elaborate":
        #     aspect_processing_func = self._elaborate_aspect

        result_queries = []
        for query in tqdm(self.query_list, desc="Processing queries", unit="query"):
            curr_query = Query(description=query)

            # extract aspects
            nav_cons, range_cons, nav_pref, subj_cons, subj_pref, infer_aspect = self._extract_aspects(query=query)

            # add aspects to current query
            for n in nav_cons:
                aspect = Navigational_Constraint(description=n)
                curr_query.add_aspect(aspect)
                
            for r in range_cons:
                price = Range_Constraint(description="price")
                price.value = r["price"]
                curr_query.add_aspect(price)
                distance = Range_Constraint(description="distance")
                distance.value = r["distance"]
                curr_query.add_aspect(distance)
            
            for n in nav_pref:
                aspect = Navigational_Preference(description=n)
                curr_query.add_aspect(aspect)
            
            for c in subj_cons:
                aspect = Subjective_Constraints(description=c)
                curr_query.add_aspect(aspect)
                
            for p in subj_pref:
                aspect = Subjective_Preference(description=p)
                curr_query.add_aspect(aspect)
                
            for i in infer_aspect:
                aspect = Inferenced_Aspect(description=i)
                curr_query.add_aspect(aspect)
                
            # if aspect_processing_func is not None:
            #     for aspect in curr_query.get_all_aspects():
            #         new_desc = aspect_processing_func(query_aspect=aspect.description)
            #         aspect.set_new_description(new_description=new_desc)
            
            result_queries.append(curr_query)

        self._save_results(result=result_queries)
        return result_queries
    
    def _load_queries(self, input_path: str) -> list[str]:
        """
        """
        with open(input_path, "r") as f:
            queries = [line.strip().lower() for line in f]
        return queries
    
    def _save_results(self, result: list[Query]):
        """
        """
        pkl_path = os.path.join(self.output_dir, f"processed_queries.pkl")
        with open(pkl_path, "wb") as f:
            pickle.dump(result, f)

        queries_data = []
        for query in result:
            query_info = {
                "Query": query.get_description(),
                "Navigational Constraints": [
                    navigation.get_original_description()
                    for navigation in query.get_navigational_constraints()
                ],
                "Range Constraints": [
                    {range.get_original_description() : range.value}
                    for range in query.get_range_constraints()
                ],
                "Navigational Preferences": [
                    navigation.get_original_description()
                    for navigation in query.get_navigational_preference()
                ],
                "Subjective Constraints": [
                    preference.get_original_description()
                    for preference in query.get_subjective_constraints()
                ],
                "Subjective Preferences": [
                    preference.get_original_description()
                    for preference in query.get_subjective_preferences()
                ],
                "Inferenced Aspects": [
                    inference.get_original_description()
                    for inference in query.get_inferenced_aspect()
                ]
            }
            queries_data.append(query_info)

        # Convert sets to lists
        for query in queries_data:
            for key, value in query.items():
                if isinstance(value, set):
                    query[key] = list(value)

        print(queries_data)

        json_path = os.path.join(self.output_dir, "processed_queries.json")
        with open(json_path, 'w') as f:
            json.dump(queries_data, f, indent=4)
        
    def _extract_aspects(self, query: str) -> tuple[list[str], list[str], list[str]]:
        """
        Extract preferences and constraints from the query
        """
        # actual prompt
        # Corrected prompt string
        # define the prompt
        prompt = """
        Instruction: Given a user query about in-car travel destination recommendations, please categorize components of the query into the following objective and subjective aspect types. For range constraints, it's a special category where the constraints are stored as a list of two values to represent a range. Each entry must always have both 'price' and 'distance' as keys, and have its lower and upper bound as values. Always convert values to kilometers for distance constraints, and always use dollars for price unit. However, if the price or the distance ranges are not specified, follow instructions for choosing presumed values. If no relevant query component about distance or price, leave them default as None. Each aspect should be expressed in its minimal form and should not be further divisible to ensure clarity and precision in the recommendation process:

        Objective:
        1. "Navigational Constraints" - Hard, factual requirements about the location, type of point of interest, and features.
            Example: If a user requests a "hotel in downtown Toronto that has a pool," the constraint is "hotel", "in downtown Toronto" and "has a pool."
        2. "Range Constraints" - Quantifiable limits on distance and price. 
            Example: A request for "a hotel under $200 per night, within 10 miles of the city center" will be broken down into "price": (0, 200) and "distance": (0, 16.09).
        3. "Navigational Preferences" - Preferred but flexible factual attributes about the location or type of the destination. 
            Example: Preferring "a hotel with a pool" is a navigational preference if not mandatory.

        Subjective:
        1. "Constraints" - Mandatory requirements based on personal or emotional needs that must be met. 
            Example: Needing a "quiet room" due to sensitivity to noise.
        2. "Preferences" - Desirable but negotiable personal or emotional desires. 
            Example: Preferring "a hotel with vibrant nightlife nearby" would be a subjective preference.
        3. "Inferenced Aspects" - Making logical deductions or inferences about unstated needs based on the query's context. 
            Example: Asking for places "similar to McDonald's" would require further inferences about what 'similar' means.

        Instructions for choosing presumed values:
            - For distance: If words like 'near' or 'nearby' are stated without specific distances, use "distance": [0,5] as the presumed tuple. If 'walking distance' or 'walkable distance', use [0,1]. If a time is specified for walking, driving, or any other transportation method, use your best judgement for distance in kilometers.
            - For price: If words like 'cheap' or 'budget', presume values to "price": [0,10] for restaurants, [0,100] for accomodations, [0,100] for any other categories. If words like 'luxurious', 'upper class' or 'top grade', presume values to [50, 9999] for restaurants, [300, 9999] for accomodations, [100, 9999] for other categories. For other words, use your best judgement and use the stated presumption rules as a reference.

        Output Requirements: Provide your answer strictly following the given JSON format. For range constraints, each entry should have both 'price' and 'distance' as keys, and have a tuple for the range of values it can take. However, if the price or the distance ranges are not specified, follow instructions for choosing presumed values. If no relevant query component about distance or price, leave them default as None. Here is the JSON structure you should use: 
        {{
            "answer": {{
                "objective": {{
                    "navigational constraints": [],
                    "range constraints": [
                        {{"distance": None}}, 
                        {{"price": None}}
                    ],
                    "navigational preferences": [],
                }}
                "subjective": {{
                    "constraints": [],
                    "preferences": [],
                    "inferenced aspects": []
                }}
            }}
        }}
        """

        # define answer format
        answer = ANSWER_FORMAT

        # few-shots
        message = [
            {"role": "system", "content": "You are an expert in answering in-car travel recommendation-style questions."},
            {"role": "system", "content": prompt},
            
            # examples
            {"role": "user", "content": "I need a hotel near the financial district of Toronto that has free parking and is under $150 per night."},
            {"role": "assistant", "content": answer.format(answer=json.dumps({"objective": {"navigational constraints": ["hotel", "near the financial district of Toronto", "has free parking"], "range constraints": [{"distance": [0, 5], "price": [0, 150]}], "navigational preferences": []}, "subjective": {"constraints": [], "preferences": [], "inferenced aspects": []}}))},
            {"role": "user", "content": "Find a budget hotel close to Toronto Pearson Airport with shuttle service and breakfast included."},
            {"role": "assistant", "content": answer.format(answer=json.dumps({"objective": {"navigational constraints": ["budget hotel", "close to Toronto Pearson Airport", "with shuttle service", "breakfast included"], "range constraints": [{"distance": [0, 5], "price": [0, 100]}], "navigational preferences": []}, "subjective": {"constraints": [], "preferences": [], "inferenced aspects": []}}))},
            {"role": "user", "content": "I'm looking for a luxury dining experience near the CN Tower, ideally with a panoramic view."},
            {"role": "assistant", "content": answer.format(answer=json.dumps({"objective": {"navigational constraints": ["luxury dining experience", "near the CN Tower"], "range constraints": [{"distance": [0, 5], "price": [50, 9999]}], "navigational preferences": ["with a panoramic view"]}, "subjective": {"constraints": [], "preferences": [], "inferenced aspects": []}}))},
            {"role": "user", "content": "Find me a restaurant similar to The Keg that has good vegetarian options."},
            {"role": "assistant", "content": answer.format(answer=json.dumps({"objective": {"navigational constraints": ["restaurant"], "range constraints": [{"distance": None, "price": [30, 50]}], "navigational preferences": ["has good vegetarian options"]}, "subjective": {"constraints": [], "preferences": [], "inferenced aspects": ["similar to The Keg"]}}))},
            {"role": "user", "content": "Can you recommend a pet-friendly accommodation within walking distance of High Park in Toronto?"},
            {"role": "assistant", "content": answer.format(answer=json.dumps({"objective": {"navigational constraints": ["pet-friendly accommodation", "within walking distance of High Park in Toronto"], "range constraints": [{"distance": [0, 1], "price": None}], "navigational preferences": []}, "subjective": {"constraints": [], "preferences": [], "inferenced aspects": []}}))},
            {"role": "user", "content": "Find me a quiet bookstore that serves coffee, ideally near the University of Toronto."},
            {"role": "assistant", "content": answer.format(answer=json.dumps({"objective": {"navigational constraints": ["bookstore", "serves coffee", "near the University of Toronto"], "range constraints": [{"distance": [0, 5], "price": None}], "navigational preferences": []}, "subjective": {"constraints": ["quiet"], "preferences": [], "inferenced aspects": []}}))},
            {"role": "user", "content": "Where can I find an upscale Italian restaurant in downtown Toronto that's good for a date night?"},
            {"role": "assistant", "content": answer.format(answer=json.dumps({"objective": {"navigational constraints": ["upscale Italian restaurant", "in downtown Toronto"], "range constraints": [{"distance": None, "price": [50, 9999]}], "navigational preferences": []}, "subjective": {"constraints": [], "preferences": ["good for a date night"], "inferenced aspects": []}}))},

            {"role": "user", "content": query},
        ]
        
        # print("\n--------------")
        # print("message:")
        # print(message)
        
        response = self.llm.generate(message)
        
        print("\n\n")
        print("Response:", response)
        print("\n\n")

        try:
            start, end = response.find("{"), response.rfind("}") + 1
            answer = json.loads(response[start:end])["answer"]
            print("answer:")
            print(answer)
            nav_cons = answer["objective"]["navigational constraints"]
            range_cons = answer["objective"]["range constraints"]
            nav_pref = answer["objective"]["navigational preferences"]
            subj_cons = answer["subjective"]["constraints"]
            subj_pref = answer["subjective"]["preferences"]
            infer_aspect = answer["subjective"]["inferenced aspects"]
            return nav_cons, range_cons, nav_pref, subj_cons, subj_pref, infer_aspect

        except json.JSONDecodeError as e:
            print(f"\nFailed to parse JSON from response")
            print("GPT answer: ", answer)
            raise e

        except Exception as e:
            print(f"\nFailed to extract constraints")
            print("GPT answer: ", answer)
            raise e


    # def _reformulate_aspect(self, query_aspect: str) -> str:
    #     """
    #     Reformulate one aspect of the query
    #     """
    #     prompt = """
    #     Given the specified aspect of a user's travel cities recommendation query, generate one sentence reformulation of the aspect to better reflect the user's intent. 
    #     Provide your answers in valid JSON format with double quote: {{"answer": "YOUR ANSWER"}}.
        
    #     Aspect: {aspect}
    #     """

    #     # define answer format
    #     answer = ANSWER_FORMAT

    #     message = [
    #         {"role": "system", "content": "You are a travel expert."},
    #         {"role": "user", "content": prompt.format(aspect="suitable for adventure seekers")},
    #         {"role": "assistant", "content": answer.format(answer="Which cities are best suited for adventure seekers looking for thrilling activities?")},
    #         {"role": "user", "content": prompt.format(aspect="has historical sites")},
    #         {"role": "assistant", "content": answer.format(answer="Which cities are rich in historical sites and cultural heritage?")},          
    #         {"role": "user", "content": prompt.format(aspect="on Asia")},
    #         {"role": "assistant", "content": answer.format(answer="Which cities in Asia are recommended for travelers?")},  
    #         {"role": "user", "content": prompt.format(aspect=query_aspect)},
    #     ]
        
    #     response = self.llm.generate(message)

    #     # parse response
    #     return correct_and_extract(response)
        

    # def _expand_aspect(self, query_aspect: str) -> str:
    #     """
    #     Expand one aspect of the query
    #     """
    #     prompt = """
    #     Given the specified aspect of a user's travel cities recommendation query, generate a list of three similar but improved descriptions of the aspect to better reflect the user's intent. 
    #     Provide your answers in valid JSON format with double quote: {{"answer": []}}.

    #     Aspect: {aspect}
    #     """
    #     # define answer format
    #     answer = ANSWER_FORMAT

    #     message = [
    #         {"role": "system", "content": "You are a travel expert."},
    #         {"role": "user", "content": prompt.format(aspect="suitable for adventure seekers")},
    #         {"role": "assistant", "content": answer.format(answer=["Ideal for outdoor adventure enthusiasts.", "Great for those seeking thrilling adventure activities.", "Perfect for adventure seekers looking for excitement and challenges."])},
    #         {"role": "user", "content": prompt.format(aspect="has historical sites")},
    #         {"role": "assistant", "content": answer.format(answer=["Rich in historical landmarks and museums.", "Offers a wealth of cultural and historical sites.", "Filled with historical attractions and heritage sites."])},          
    #         {"role": "user", "content": prompt.format(aspect="on Asia")},
    #         {"role": "assistant", "content": answer.format(answer=["Located in Asia.", "Situated in Asia.", "In Asia."])},  
    #         {"role": "user", "content": prompt.format(aspect=query_aspect)},
    #     ]

    #     response = self.llm.generate(message)

    #      # parse response
    #     return correct_and_extract(response)

    # def _elaborate_aspect(self, query_aspect: str) -> str:
    #     """
    #     Elaborate one aspect of the query
    #     """
    #     prompt = """
    #     Given the specified aspect of a user's travel cities recommendation query, generate one paragraph specific definition of the aspect. 
    #     Provide your answers in valid JSON format with double quote: {{"answer": "YOUR ANSWER"}}.
        
    #     Aspect: {aspect}
    #     """

    #     # define answer format
    #     answer = ANSWER_FORMAT

    #     message = [
    #         {"role": "system", "content": "You are a travel expert."},
    #         {"role": "user", "content": prompt.format(aspect="suitable for adventure seekers")},
    #         {"role": "assistant", "content": answer.format(answer="Cities that are suitable for adventure seekers are those that offer a variety of thrilling and exciting activities tailored to those who crave physical challenges and adrenaline-pumping experiences. These cities often feature natural landscapes that allow for activities like hiking, climbing, white-water rafting, and skydiving. Additionally, they might host adventure parks or offer unique local experiences such as jungle expeditions or desert safaris. Such destinations are designed to cater to the adventurous spirit, providing not just activities but also the necessary safety measures and facilities to ensure a memorable and exhilarating visit.")},
    #         {"role": "user", "content": prompt.format(aspect="has historical sites")},
    #         {"role": "assistant", "content": answer.format(answer="Cities that are noted for having historical sites are rich in monuments, ruins, and museums that chronicle significant past events and cultures. These cities serve as gate-banners of history, often featuring well-preserved architecture, ancient artifacts, and UNESCO World Heritage sites that attract scholars, history enthusiasts, and tourists alike. The presence of these historical sites adds a deep cultural layer to the city, offering visitors a tangible connection to the past and an opportunity to learn about the historical narratives that shaped the modern world. Such cities often provide guided tours, educational programs, and interactive exhibits to enhance the visitor experience.")},          
    #         {"role": "user", "content": prompt.format(aspect="has Disney")},
    #         {"role": "assistant", "content": answer.format(answer= "Cities with Disney theme parks are renowned destinations that promise magical experiences for visitors of all ages. Anaheim, California, is home to Disneyland Resort, the original Disney theme park, offering classic attractions and the newer Star Wars: Galaxy’s Edge. Orlando, Florida, hosts Walt Disney World Resort, the largest Disney park globally, featuring four theme parks and two water parks. Tokyo, Japan, provides a unique twist with Tokyo Disney Resort, including Tokyo Disneyland and Tokyo DisneySea, known for its high attention to detail and cultural adaptations. Paris, France, offers Disneyland Paris, blending Disney magic with European flair. These cities not only draw Disney enthusiasts but also offer comprehensive family entertainment, making them top choices for Disney-themed vacations.")},  
    #         {"role": "user", "content": prompt.format(aspect=query_aspect)},
    #     ]

    #     response = self.llm.generate(message)

    #     # parse response
    #     return correct_and_extract(response)
        

# def correct_and_extract(input_string) -> str:
#     """
#     Extracts the content within curly braces and corrects the 'answer' key-value pair.
#     """
#     pattern = r"\{([^}]*)\}"
#     extracted_content = re.search(pattern, input_string)

#     if not extracted_content:
#         return "No content in curly braces found."

#     content_within_braces = extracted_content.group(1)

#     answer_pattern = r"(\s*\"?answer\"?\s*)(:)\s*(.*)"

#     def replacer(match):
#         key = '"answer":'  
#         value = match.group(3).strip().strip("'\"")
#         value = '"' + value.replace('"', '\\"') + '"'
#         return f"{key} {value}"
    
#     corrected_content = re.sub(answer_pattern, replacer, content_within_braces, flags=re.IGNORECASE)

#     try:
#         json_string = '{' + corrected_content + '}'
#         corrected_dict = json.loads(json_string)
#         return corrected_dict.get('answer', 'No valid "answer" found')
#     except json.JSONDecodeError as e:
#         return f'Correction failed; the string might still be invalid. Error: {str(e)}'