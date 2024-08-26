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
            obj_cons, range_cons, obj_pref, dir_subj_cons, indir_subj_cons, dir_subj_pref, indir_subj_pref = self._extract_aspects(query=query)

            # add aspects to current query
            for n in obj_cons:
                aspect = Objective_Constraint(description=n)
                curr_query.add_aspect(aspect)
                
            for r in range_cons:
                price = Range_Constraint(description="price")
                price.value = r["price"]
                curr_query.add_aspect(price)
                distance = Range_Constraint(description="distance")
                distance.value = r["distance"]
                curr_query.add_aspect(distance)
            
            for n in obj_pref:
                aspect = Objective_Preference(description=n)
                curr_query.add_aspect(aspect)
            
            for c in dir_subj_cons:
                aspect = Direct_Subjective_Constraints(description=c)
                curr_query.add_aspect(aspect)
                
            for p in dir_subj_pref:
                aspect = Direct_Subjective_Preference(description=p)
                curr_query.add_aspect(aspect)
                
            for i in indir_subj_cons:
                goals = self._decompose(i)
                print(goals)
                aspect = Indirect_Aspect(description=i, goals=goals)
                aspect.goals = goals
                curr_query.add_aspect(aspect)
                
            for i in indir_subj_pref:
                goals = self._decompose(i)
                print(goals)
                aspect = Indirect_Aspect(description=i, goals=goals)
                aspect.goals = goals
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
                "Objective Constraints": [
                    navigation.get_original_description()
                    for navigation in query.get_navigational_constraints()
                ],
                "Range Constraints": [
                    {range.get_original_description() : range.value}
                    for range in query.get_range_constraints()
                ],
                "Objective Preferences": [
                    navigation.get_original_description()
                    for navigation in query.get_navigational_preference()
                ],
                "Direct Subjective Constraints": [
                    preference.get_original_description()
                    for preference in query.get_dir_subjective_constraints()
                ],
                "Direct Subjective Preferences": [
                    preference.get_original_description()
                    for preference in query.get_dir_subjective_preferences()
                ],
                "Indirect Aspects": [
                    (indirect.get_original_description(), indirect.goals)
                    for indirect in query.get_indirect_aspects()
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
        Instructions: Given a user query about in-car travel destination recommendations, please follow instruction by steps and categorize components of the query into the following aspect taxonomy. 
        
        1. Find all aspects in the query
        2. From all aspects, see if there are range constraints, which is a special category where the constraints are stored as a list of two values to represent a range. Each entry must always have both 'price' and 'distance' as keys, and have its lower and upper bound as values. Always convert values to kilometers for distance constraints, and always use dollars for price unit. However, if the price or the distance ranges are not specified, follow instructions for choosing presumed values. If no relevant query component about distance or price, leave them default as None. 
        3. Categorize all aspects into the following taxonomy of query aspects. Make sure to reference 'Instructions to differentiate between constraint and preference', 'Instruction to differentiate between objective and subjective', and 'Instruction to differentiate between direct and indirect aspects' when processing each aspect.
        4. Besides aspects categorized as indirect, strictly simplify all aspects to key words. Each aspect should be expressed in its minimal form and captures only the keywords in a phrase to ensure clarity and precision in the recommendation process. For example, 'have a pool' should be reduced to just 'pool'. On the other hand, Indirect Aspects can allow a more complete phrase.

        Taxonomy:
        - Objective:
        1. "Objective Constraints" - Hard, factual requirements about the location, type of point of interest, and features.
            Example: If a user requests a "hotel in downtown Toronto that has a pool," the constraint is "hotel", "in downtown Toronto" and "has a pool."
        2. "Range Constraints" - Quantifiable limits on distance and price. 
            Example: A request for "a hotel under $200 per night, within 10 miles of the city center" will be broken down into "price": (0, 200) and "distance": (0, 16.09).
        3. "Objective Preferences" - Preferred but flexible factual attributes about the location or type of the destination. 
            Example: Preferring "a hotel with a pool" is a navigational preference if not mandatory.

        - Subjective:
        1. "Direct Subjective Constraints" - These aspects are still direct but involve a level of personal judgment or preference, even though they can be clearly identified and are often based on common understanding or standards:
            Examples:
                - Taste of Food: Restaurants may be rated for having "excellent" or "poor" food based on culinary reviews or customer ratings, which, while subjective, are direct assessments.
                - Comfort of Bedding: Often rated in guest reviews, which subjectively assess comfort but are directly stated.
                - Quality of Service: Described through direct feedback like "friendly" or "unresponsive," reflecting personal experiences.
        2. "Indirect Subjective Constraints" - These aspects imply broader themes or deeper meanings that require interpretation and cannot be directly quantified without subjective judgment:
            Examples:
                - Romantic Atmosphere: A subjective quality suggesting an overall feeling or ambiance, needing decomposition into aspects like candlelit dinners, secluded settings, etc.
                - Family-Friendly Environment: Suggests a setting suitable for children but requires interpretation of features like kid’s activities, safety measures, and family-oriented services.
                - Luxurious Experience: Indicates a high standard of comfort and elegance, needing further interpretation to link with services like spa treatments, gourmet dining, and concierge services.
                - More Examples: 'eco-friendly','pet-friendly', 'family-friendly', 'meaningful experience for kids', 'gourmet dining', 'similar to McDonald's', 'a relaxing vibe', 'family-gathering', 'allergic to dust', 'nightlife'
        3. "Direct Subjective Preferences" - These aspects are still direct but involve a level of personal judgment or preference, even though they can be clearly identified and are often based on common understanding or standards:
            Examples:
                - Taste of Food: Restaurants may be rated for having "excellent" or "poor" food based on culinary reviews or customer ratings, which, while subjective, are direct assessments.
                - Comfort of Bedding: Often rated in guest reviews, which subjectively assess comfort but are directly stated.
                - Quality of Service: Described through direct feedback like "friendly" or "unresponsive," reflecting personal experiences.
        4. "Indirect Subjective Preferences" - These aspects imply broader themes or deeper meanings that require interpretation and cannot be directly quantified without subjective judgment:
            Examples:
                - Romantic Atmosphere: A subjective quality suggesting an overall feeling or ambiance, needing decomposition into aspects like candlelit dinners, secluded settings, etc.
                - Family-Friendly Environment: Suggests a setting suitable for children but requires interpretation of features like kid’s activities, safety measures, and family-oriented services.
                - Luxurious Experience: Indicates a high standard of comfort and elegance, needing further interpretation to link with services like spa treatments, gourmet dining, and concierge services.
                - More Examples: 'eco-friendly','pet-friendly', 'family-friendly', 'meaningful experience for kids', 'gourmet dining', 'similar to McDonald's', 'a relaxing vibe', 'family-gathering', 'allergic to dust', 'nightlife'
        
        Instructions for choosing presumed values:
            - For distance: If words like 'near' or 'nearby' are stated without specific distances, use "distance": [0,5] as the presumed tuple. If 'walking distance' or 'walkable distance', use [0,1]. If a time is specified for walking, driving, or any other transportation method, use your best judgement for distance in kilometers.
            - For price: If words like 'cheap' or 'budget', presume values to "price": [0,10] for restaurants, [0,100] for accomodations, [0,100] for any other categories. If words like 'luxurious', 'upper class' or 'top grade', presume values to [50, 9999] for restaurants, [300, 9999] for accomodations, [100, 9999] for other categories. For other words, use your best judgement and use the stated presumption rules as a reference.

        Instructions to differentiate between constraint and preference:
            - A constraint is a non-negotiable requirement essential for user needs, like health or safety, and is implied by a serious or necessary tone in the query (e.g., "I need a hotel with wheelchair accessibility"). A preference is more flexible, enhancing user satisfaction without being essential, often indicated by a more casual tone (e.g., "I’d like a hotel with a swimming pool"). Determine the classification based on whether the aspect is depicted as mandatory or merely desirable.
        
        Instruction to differentiate between objective and subjective:
            - An objective aspect is based on measurable, factual, or universally accepted criteria that remain constant, such as the amenities in a hotel (e.g., "I want a hotel with an outdoor pool"). A subjective aspect depends on personal feelings or opinions, which vary between individuals, such as the comfort of a hotel room (e.g., "I need a hotel with a comfortable room"). Classify the aspect by assessing if it is quantifiable and universally applicable, or if it varies based on individual perception, often expressed through descriptive adjectives.
        
        Instruction to differentiate between direct and indirect aspects:
            - Direct Aspects are specific, factual features or attributes that are straightforward to identify and verify using standard metadata from sources like hotel or restaurant listings and reviews. They do not benefit from further decomposition or expansion when matching with existing data, as they contain no hidden meanings and do not imply additional messages beyond their explicit presentation. In our definition, all of objective aspects are direct since they by nature do not have controversial or hidden meanings.
            - Indirect Aspects are overarching themes or missions that are somewhat broad or abstract to directly match metadata in hotel/restaurant listings or reviews. It is helpful from them to be decomposed into more specific, actionable components that align with available data. This category should include any high-level descriptor that suggests a lifestyle, ethos, or specific type of experience that cannot be directly quantified or verified without interpretation.

        Output Requirements: Provide your answer strictly following the given JSON format. For range constraints, each entry should have both 'price' and 'distance' as keys, and have a tuple for the range of values it can take. However, if the price or the distance ranges are not specified, follow instructions for choosing presumed values. If no relevant query component about distance or price, leave them default as None. Here is the JSON structure you should use: 
        {{
            "answer": {{
                "objective": {{
                    "objective constraints": [],
                    "range constraints": [
                        {{"distance": None}}, 
                        {{"price": None}}
                    ],
                    "objective preferences": [],
                }}
                "subjective": {{
                    "direct subjective constraints": [],
                    "indirect subjective constraints": [],
                    "direct subjective preferences": [],
                    "indirect subjective preferences": []
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
            {"role": "user", "content": "I need a bed and breakfast near the lake, ideally in a quiet area."},
            {"role": "assistant", "content": answer.format(answer=json.dumps({"objective": {"objective constraints": ["bed and breakfast", "lake"], "range constraints": [{"distance": [0, 5], "price": None}], "objective preferences": []}, "subjective": {"direct subjective constraints": [], "indirect subjective constraints": [], "direct subjective preferences": ["quiet area"], "indirect subjective preferences": []}}))},

            {"role": "user", "content": "Looking for a boutique hotel downtown, ideally with a rooftop bar."},
            {"role": "assistant", "content": answer.format(answer=json.dumps({"objective": {"objective constraints": ["boutique hotel", "downtown"], "range constraints": [{"distance": None, "price": None}], "objective preferences": ["rooftop bar"]}, "subjective": {"direct subjective constraints": [], "indirect subjective constraints": [], "direct subjective preferences": [], "indirect subjective preferences": []}}))},

            {"role": "user", "content": "I need a hotel that is environmentally responsible and near the beach."},
            {"role": "assistant", "content": answer.format(answer=json.dumps({"objective": {"objective constraints": ["hotel", "beach"], "range constraints": [{"distance": [0, 5], "price": None}], "objective preferences": []}, "subjective": {"direct subjective constraints": [], "indirect subjective constraints": ["environmentally responsible"], "direct subjective preferences": [], "indirect subjective preferences": []}}))},

            {"role": "user", "content": "Looking for a dining experience in a place that supports local farmers and has a view of the mountains."},
            {"role": "assistant", "content": answer.format(answer=json.dumps({"objective": {"objective constraints": ["dining experience", "mountains"], "range constraints": [{"distance": None, "price": None}], "objective preferences": []}, "subjective": {"direct subjective constraints": [], "indirect subjective constraints": ["supports local farmers"], "direct subjective preferences": [], "indirect subjective preferences": []}}))},

            {"role": "user", "content": "Can you find a cozy café that has a rustic vibe and serves organic coffee?"},
            {"role": "assistant", "content": answer.format(answer=json.dumps({"objective": {"objective constraints": ["cozy café", "organic coffee"], "range constraints": [{"distance": None, "price": None}], "objective preferences": []}, "subjective": {"direct subjective constraints": [], "indirect subjective constraints": [], "direct subjective preferences": [], "indirect subjective preferences": ["rustic vibe"]}}))},

            {"role": "user", "content": "I want to stay at a resort that feels like a home away from home, ideally where I can also bring my dog."},
            {"role": "assistant", "content": answer.format(answer=json.dumps({"objective": {"objective constraints": ["resort"], "range constraints": [{"distance": None, "price": None}], "objective preferences": []}, "subjective": {"direct subjective constraints": [], "indirect subjective constraints": ["home away from home"], "direct subjective preferences": [], "indirect subjective preferences": ["can bring my dog"]}}))},

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
            obj_cons = answer["objective"]["objective constraints"]
            range_cons = answer["objective"]["range constraints"]
            obj_pref = answer["objective"]["objective preferences"]
            dir_subj_cons = answer["subjective"]["direct subjective constraints"]
            indir_subj_cons = answer["subjective"]["indirect subjective constraints"]
            dir_subj_pref = answer["subjective"]["direct subjective preferences"]
            indir_subj_pref = answer["subjective"]["indirect subjective preferences"]
            return obj_cons, range_cons, obj_pref, dir_subj_cons, indir_subj_cons, dir_subj_pref, indir_subj_pref

        except json.JSONDecodeError as e:
            print(f"\nFailed to parse JSON from response")
            print("GPT answer: ", answer)
            raise e

        except Exception as e:
            print(f"\nFailed to extract constraints")
            print("GPT answer: ", answer)
            raise e



    ### Expansion

    def _decompose(self, indirect_aspect: str):
        prompt = """
        1. Given a high-level mission, decompose the mission into lower-level goals. The mission is extracted from a user query in the in-car travel context. The goals should capture the implications of user needs and should be at a level where they are likely to have direct matches in hotel/restaurant descriptions, amenities and reviews. 
        2. To have a higher-chance of being matched, simplify the goals to capture only the keywords. For example, 'educational programs' should just be 'education', and 'massage services' should only be 'massage'.
        3. If the high-level mission itself is also likely to have a match, include it in its decomposed goals as well, like 'pet-friendly' and 'eco-friendly'.
        4. Output a list of strings for the goals.
        """

        # few-shots
        message = [
            {"role": "system", "content": "You are a human intelligence agent."},
            {"role": "system", "content": prompt},
            
            # examples
            {"role": "user", "content": "stay healthy"},
            {"role": "assistant", "content": "gym, spa, vegetarian, non-smoking, fitness, outdoor activities, quality sleep"},
            {"role": "user", "content": "relaxing getaway"},
            {"role": "assistant", "content": "spa, massage, quiet, scenic view, hot tub, garden"},
            {"role": "user", "content": "business trip"}, 
            {"role": "assistant", "content": "Wi-Fi, meeting rooms, desk, airport shuttle, conference center, express check-out"},
            {"role": "user", "content": "family vacation"}, 
            {"role": "assistant", "content": "kid-friendly, children's menu, family rooms, pool, entertainment, childcare"},
            {"role": "user", "content": "gourmet dining"}, 
            {"role": "assistant", "content": "Michelin-star, gourmet, chef's table, tasting menu, wine, fine dining"},
            {"role": "user", "content": "pet-friendly"}, 
            {"role": "assistant", "content": "pet-friendly, dog park, pet services, welcome pets, dog bed, pet menu"},
            {"role": "user", "content": "eco-friendly"},
            {"role": "assistant", "content": "eco-friendly, solar power, recycling, organic, green, energy-efficient, sustainable"},
            
            {"role": "user", "content": indirect_aspect},
        ]
        
        # print("\n--------------")
        # print("message:")
        # print(message)
        
        response = self.llm.generate(message)
        
        print("\n\n")
        print("Response:", response)
        print("\n\n")
        
        return response