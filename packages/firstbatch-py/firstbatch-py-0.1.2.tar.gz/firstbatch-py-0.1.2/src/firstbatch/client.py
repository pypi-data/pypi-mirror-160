from firstbatch.request_handler import FirstBatchRequests
from firstbatch.utils import FirstBatchEvent, EventTypes, StateEnum


class FirstBatchClient:
    def __init__(self, public_key, secret):
        self.__requests = FirstBatchRequests()
        self.__public_key = public_key
        self.__secret = secret
        self.__bearer_token = self.__requests.call_auth(signed_hash=self.__requests.auth_sign(self.__secret),
                                                        public_key=self.__public_key)["data"]["bearer"]
        self.__requests.set_header(pk=self.__public_key, bearer=self.__bearer_token)

    def get_all_events(self):
        response = self.__requests.call_get_events()
        if not response["success"]:
            return response
        return [FirstBatchEvent(name=ev["name"], event_id=ev["event_id"], event_type=ev["event_type"],
                                state=ev["state"]) for ev in response["data"]]

    def create_event(self, name: str, event_type: EventTypes):
        response = self.__requests.call_create_event(name=name, event_type=event_type)
        if not response["success"]:
            return response
        return FirstBatchEvent(name=name, event_id=response["data"]["event_id"], event_type=event_type)

    def boot_event(self, event: FirstBatchEvent):
        return self.__requests.call_create_event_onchain(event_id=event.event_id)

    def add_gate(self, event: FirstBatchEvent):
        return self.__requests.call_add_gate(event_id=event.event_id,
                                                 group_id=event.gate_id_interest)

    def update_rules(self, event: FirstBatchEvent):
        return self.__requests.call_add_rule(event_id=event.event_id, rules=event.rules)

    def update_state(self, event: FirstBatchEvent, state: StateEnum):
        return self.__requests.call_update_event_state(event_id=event.event_id, state=state)

    def get_statistics(self, event: FirstBatchEvent):
        return self.__requests.call_event_statistics(event_id=event.event_id)

    def get_event_link(self, event: FirstBatchEvent):
        return self.__requests.call_get_event_linkt(event_id=event.event_id)

    def get_custom_persona(self):
        return self.__requests.call_get_custom_personas()

    def create_custom_persona(self, name: str, logic: str):
        return self.__requests.call_create_custom_persona(name=name, logic=logic)


