from dataclasses import dataclass
import json

@dataclass
class MatchEvent:
    event_type: str
    data: dict

    @classmethod
    def from_json(cls, json_data):
        parsed = json.loads(json_data)
        return cls(event_type=parsed['eventType'], data=parsed['data'])
    
    def to_json(self):
        return json.dumps({
            "eventType": self.event_type,
            "data": json.loads(self.data)
        })