from flask import Blueprint, jsonify, request
from core.critique.critique_service import CritiqueService
from state.state_manager import StateManager

class CritiqueResource:
    _critique_service: CritiqueService
    blueprint: Blueprint
    _state_manager: StateManager

    def __init__(self, critique_service: CritiqueService, state_manager: StateManager):
        self.blueprint = Blueprint('critique_resource', __name__)
        self._critique_service = critique_service
        self._state_manager = state_manager
        self._register_routes()

    def _register_routes(self):
        #Register routes with the blurprint
        self.blueprint.add_url_rule('/query', view_func=self.append_query_or_recommend, methods=['POST'])


    def 