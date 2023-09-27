class IdentityMap:
    def __init__(self):
        self._identity_map = {}

    def add(self, entity_type, entity_id, entity):
        if entity_type not in self._identity_map:
            self._identity_map[entity_type] = {}
        self._identity_map[entity_type][entity_id] = entity

    def get(self, entity_type, entity_id):
        return self._identity_map.get(entity_type, {}).get(entity_id)

    def update(self, entity_type, entity_id, entity):
        if (
            entity_type in self._identity_map
            and entity_id in self._identity_map[entity_type]
        ):
            self._identity_map[entity_type][entity_id] = entity

    def remove(self, entity_type, entity_id):
        if (
            entity_type in self._identity_map
            and entity_id in self._identity_map[entity_type]
        ):
            del self._identity_map[entity_type][entity_id]

    def clear(self):
        self._identity_map.clear()


class IdentityMapStub:
    def add(self, entity_type, entity_id, entity):
        pass

    def get(self, entity_type, entity_id):
        pass

    def update(self, entity_type, entity_id, entity):
        pass

    def remove(self, entity_type, entity_id):
        pass

    def clear(self):
        pass
