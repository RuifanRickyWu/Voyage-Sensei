from flask import Blueprint, jsonify, request
from core.query.query_service import QueryService
from state.state_manager import StateManager


class QueryResource:
    _query_service: QueryService
    blueprint: Blueprint
    _state_manager: StateManager

    def __init__(self, query_service, state_manager: StateManager):
        self._query_service = query_service
        self.blueprint = Blueprint('query_resource', __name__)
        self._state_manager = state_manager
        self._register_routes()

    def _register_routes(self):
        #Register routes with the blurprint
        self.blueprint.add_url_rule('/query', view_func=self.append_query_or_recommend, methods=['POST'])
        self.blueprint.add_url_rule('/query/current_plan', view_func=self.get_current_plan, methods=['GET'])

    def append_query_or_recommend(self):
        try:
            payload = request.get_json()
            query_payload = payload.get('query', '')
            print(query_payload)
            return jsonify(self._query_service.append_query_or_recommend(query_payload, self._state_manager)), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_current_plan(self):
        try:
            return jsonify(self._query_service.get_current_plan(self._state_manager)), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
