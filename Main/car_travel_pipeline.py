from CarTravel.data_process.database_service import DB_Service
from CarTravel.retriever.filtering.geo_search import GeoSearch
from CarTravel.Entity.aspect import Indirect_Aspect
import json
from CarTravel.retriever.Rank.trade_off import TradeOff
from CarTravel.retriever.Rank.rank import Rank

class CarTravel:
    _DB_Service: DB_Service
    _ranking: TradeOff
    _Geo_Search: GeoSearch

    def __init__(self, input_path: str, output_dir: str):
        self.input_path = input_path
        self.output_dir = output_dir
        self._DB_Service = DB_Service()
        self._Geo_Search = GeoSearch()

        self._ranking = TradeOff()
        self._rank = Rank()
        
        print("\n\nFinished initializing pipeline.\n\n")

    def run(self):
        self._DB_Service.create_db()

        json_path = self.output_dir
        with open(json_path, 'r') as file:
            data = json.load(file)
        evaluation = []
        for i in range(len(data)):
            print(f"Start of {i}-th query:")
            print(data[i]["Query"])
            
            # load aspects from json
            objective_constraints = data[i]["Objective Constraints"] # only testing 1st query
            objective_preferences = data[i]['Objective Preferences']
            range_constraints = data[i]['Range Constraints']
            direct_subjective_constraints = data[i]["Direct Subjective Constraints"]
            direct_subjective_preferences = data[i]["Direct Subjective Preferences"]
            indirect_aspects_raw = data[i]["Indirect Aspects"]
            indirect_aspects = []
            for aspect in indirect_aspects_raw:
                aspect_name = aspect[0]
                aspect_goals = aspect[1].split(", ")
                aspect_obj = Indirect_Aspect(aspect_name, aspect_goals)
                indirect_aspects.append(aspect_obj) # NOTE: use indirect_aspects[k].goals for list of decomposed aspects
                
            question = data[i]["Query"]
            print("\nEnd of query processor...\n")

            #pois = self._DB_Service.filter_search(navigational_constraints)
            #print("numbers of pois after filtering: " + str(len(pois)))

            print("\nStart of Ranking:")
            
            # number of ground truths for 10 indirect aspect queries
            numbers_of_ground_truths = [6,4,7,5,13,2,5,13,6,6]
            result =self._rank.rank(objective_constraints, objective_preferences, indirect_aspects, numbers_of_ground_truths[i])
            # for poi in result:
            #     print("\npoi name:")
            #     print(poi.get_name())

            #result = self._ranking.get_topk_poi_dynamic_weights(query, pois, 24)
            #list = result.get_POI_list()
            #for poi in list:
            #    print("\npoi name:")
            #    print(poi.get_name())
                #print("\ndescription:")
                #print(poi.get_description())
                #print("\nfeatures:")
                #print(poi.get_feature())
                
            print("\n\n-----------------------------------------------\nstart auto testing\n\n")
            
            #num_correct = 0
            #with open('CarTravel/Main/0_ground_truth.json', 'r', encoding='utf-8') as json_file:
            #    ground_truth_data = json.load(json_file)
            #    for sub_dictionary in ground_truth_data['questions']:
            #        if sub_dictionary['question'].lower() == question:
            #            ground_truths = sub_dictionary['answerlist']
            #            print("question: " + question + ": \n")
            #            for poi in result:
            #                if poi.get_name() in ground_truths:
            #                    print(f"{poi.get_name()} WAS a ground truth")
            #                    num_correct += 1
            #                else:
             #                   print(f"{poi.get_name()} WASN'T a ground truth")
              #          print(f"\ndone with testing for query {question}")
               #         print(f"got {num_correct}/{len(ground_truths)} correct")
               #         evaluation.append(str(num_correct) + "/" + str(len(ground_truths)))
        #print(evaluation)
                        




