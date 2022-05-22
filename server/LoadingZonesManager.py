from LoadingZone import LoadingZone

class LoadingZonesManager:
    def __init__(self) -> None:
        self.loadingZones = []

        self.add_loading_zone(10,5)
        self.add_loading_zone(11,5)
        self.add_loading_zone(10,6)
        self.add_loading_zone(11,6)
        self.add_loading_zone(10,7)
        self.add_loading_zone(11,7)

    def add_loading_zone(self, posX, posY):
        self.loadingZones.append(LoadingZone(posX, posY))