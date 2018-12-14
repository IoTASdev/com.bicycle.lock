import ast

from shapely.geometry import Polygon, Point, mapping

from user_auth import redis_client


class Stand:

    def __init__(self, stand_name, stand_coordinates, stand_centroid, stand_manager, manager_contact, no_of_bicycles):
        """
        This is an constructor for class Stand which holds initial default values of classes
        :param stand_name:
        :param stand_coordinates:
        :param stand_centroid:
        :param stand_manager:
        :param manager_contact:
        :param no_of_bicycles
        """
        self.stand_name = stand_name
        self.stand_coordinates = stand_coordinates
        self.stand_centroid = stand_centroid
        self.stand_manager = stand_manager
        self.manager_contact = manager_contact
        self.no_of_bicycles = no_of_bicycles

    def register(self, stand_name, stand_coordinates, stand_manager, manager_contact, no_of_bicycles):
        if redis_client.exists(manager_contact) is 0:
            stand_data = {
                'consumer_type': 'stand',
                'stand_name': stand_name,
                'stand_coordinates': stand_coordinates,
                'stand_manager': stand_manager,
                'manager_contact': manager_contact,
                'no_of_bicycles': no_of_bicycles
            }
            print(stand_coordinates)
            redis_client.hmset(manager_contact, stand_data)
            stand_coordinates_list = ast.literal_eval(stand_coordinates)
            print(stand_coordinates_list)
            polygon = Polygon(stand_coordinates_list)
            print(polygon)
            print(Point(polygon.representative_point().coords))
            geojson = mapping(polygon.representative_point())
            print(geojson)
            stand_ref_point = Point(geojson['coordinates'])
            print(stand_ref_point)
            print(stand_ref_point.within(polygon))
            response = {'status': 'RES_CREATED', 'message': 'Stand Registered Successfully'}
            return response
        else:
            response = {'status': 'BAD_REQUEST', 'message': 'Stand with same identifier already exists!'}
            return response

    def modify(self, stand_name, stand_coordinates, stand_centroid, stand_manager, manager_contact, no_of_bicycles):
        pass

    def delete(self, stand_name, stand_coordinates, stand_centroid, stand_manager, manager_contact, no_of_bicycles):
        pass

    def no_of_bicycles(self, stand_name, stand_coordinates, stand_centroid, stand_manager, manager_contact, no_of_bicycles):
        """

        :param stand_name:
        :param stand_coordinates:
        :param stand_centroid:
        :param stand_manager:
        :param manager_contact:
        :param no_of_bicycles:
        """
        pass

    def validate_stand_area(self,stand_name, stand_coordinates, stand_centroid, stand_manager, manager_contact, no_of_bicycles):
        pass

    def nearby_stands(self, stand_name, stand_coordinates, stand_centroid, stand_manager, manager_contact, no_of_bicycles):
        pass