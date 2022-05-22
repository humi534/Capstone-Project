
import Package


class PackagesManager:

    def __init__(self) -> None:
        self.available_packages = []
        self.moving_packages = []
        self.delivered_packages = []
        self.still_products = True
        
    
    def get_package(self, type_package, product_id):
        for package in type_package:
            if package.product_id == product_id:
                return package
        raise Exception("error: The package ", product_id, " was not detected")
        
    def check_id_in_typelist(self, type_package, product_id) -> bool:
        for package in type_package:
            if package.product_id == product_id:
                return True
        return False
        
    def add_package(self, product_id, destination, posX, posY) -> None:
        """Ajoute un parcel dans available"""
        self.available_packages.append(Package.Package(product_id, destination, posX, posY))
    
    def add_moving_package(self, product_id) -> None:
        """Deplace de available vers moving"""
        if not self.check_id_in_typelist(self.moving_packages, product_id):
            if self.check_id_in_typelist(self.available_packages, product_id):
                package = self.get_package(self.available_packages, product_id)
                print("package into available", package.toString())
                self.moving_packages.append(package)
                for i in self.moving_packages:
                    print(i.toString())
                self.available_packages.remove(package)
        
    def add_delivered_package(self, product_id) -> None:
        if not self.check_id_in_typelist(self.delivered_packages, product_id):
            if self.check_id_in_typelist(self.moving_packages, product_id):
                package = self.get_package(self.moving_packages, product_id)
                self.delivered_packages.append(package)
                self.moving_packages.remove(package)
    
    def change_still_products(self):
        if not self.available_packages: #if list empty
            self.still_products = False
        else:
            self.still_products = True
    
    def get_still_products(self):
        return self.still_products