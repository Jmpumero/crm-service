import statistics
import functools
from datetime import datetime, timedelta
from typing import Any, Optional

from fastapi import status
from fastapi.responses import JSONResponse

from ..schemas.response.customers_sensors import PmsBooking, PmsResponse, PmsHistory
from src.customer.profile_sensors_endpoint.repository.pms import PmsQueries

class PmsService(PmsQueries):
    '''
    Service to get PMS usage statistics
     
    '''
    def __init__(self):
        super().__init__()


    async def get_pms_stats(self, customer_id, sensor):
        masters_list = []
        books_list = []
        stay_time_list = []
        used_room_type_list = []
        incomes_list = []
        nights_list = []
        anticipation_list = []
        cancellation_list = []
        sales_channels_list = []

        customer_reservations = self.get_all_customer_stays(customer_id)
        

        #ESTADIA PROMEDIO
        async for master in customer_reservations:
            masters_list.append(master)
        
        for master in masters_list:
            master_reservation_creation_date = datetime.strptime(master['data']['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
            master_reservation_checkin_date = datetime.strptime(master['data']['checkin'], "%Y-%m-%d")
            anticipation_time = master_reservation_checkin_date - master_reservation_creation_date
            anticipation_list.append(anticipation_time.days)
            
            for book in master['data']['bBooks']:
                books_list.append(book)
                incomes_list.append(book['netAmt'])
                nights_list.append(book['nights'])
                
                checkout_date = datetime.strptime(book['checkout'], '%Y-%m-%d')
                checkin_date = datetime.strptime(book['checkin'], '%Y-%m-%d')
                
                stay_time = checkout_date - checkin_date
                stay_time_list.append(stay_time.days)

        async for type in self.group_by_most_used_roomType(customer_id):
            used_room_type_list.append(type)

        # async for anticipation in self.get_avg_anticipation(customer_id):
        #     print(anticipation)
        #     anticipation_list.append(anticipation)

        async for cancellation in self.get_cancellations(customer_id):
            if cancellation['_id'][0] == 'cancelled':
                cancellation_list.append(cancellation)

        async for channel in self.get_preferred_sale_channel(customer_id):
            sales_channels_list.append(channel)

        #RESUMEN GLOBAL

        first_lodge_checkin = datetime.strptime(masters_list[0]['data']['bBooks'][0]['checkin'], '%Y-%m-%d')
        first_lodge_checkout = datetime.strptime(masters_list[0]['data']['bBooks'][0]['checkout'], '%Y-%m-%d')
        first_lodge_property = masters_list[0]['data']['sproperty']['code']
        first_lodge_Room_type = masters_list[0]['data']['bBooks'][0]['riRoomType']['name']
        first_lodge_amount = masters_list[0]['data']['bBooks'][0]['netAmt']
        
        last_lodge_checkin = datetime.strptime(masters_list[-1]['data']['bBooks'][-1]['checkin'], '%Y-%m-%d')
        last_lodge_checkout = datetime.strptime(masters_list[-1]['data']['bBooks'][-1]['checkout'], '%Y-%m-%d')
        last_lodge_property = masters_list[-1]['data']['sproperty']['code']
        last_lodge_Room_type = masters_list[-1]['data']['bBooks'][-1]['riRoomType']['name']
        last_lodge_amount = masters_list[-1]['data']['bBooks'][-1]['netAmt']
            
        first_lodge_duration = round((first_lodge_checkout - first_lodge_checkin) / timedelta(days = 1), 2) 
        last_lodge_duration = round((last_lodge_checkout - last_lodge_checkin) / timedelta(days = 1), 2) 

        response = {
            'pms_response':{
                    'status_code':status.HTTP_200_OK,
                    'message': 'Ok'
            },
            'pms_first_stay': {
                'date': first_lodge_checkin.strftime('%Y-%m-%d'),
                'property': first_lodge_property,
                'duration': f'{first_lodge_duration} days',
                'room_type': first_lodge_Room_type,
                'amount': first_lodge_amount
            },
            'pms_last_stay': {
                'date': last_lodge_checkin.strftime('%Y-%m-%d'),
                'property': last_lodge_property,
                'duration': f'{last_lodge_duration} days',
                'room_type': last_lodge_Room_type,
                'amount': last_lodge_amount
            },
            'pms_avg_stay': round(statistics.mean(stay_time_list), 2),
            'pms_last_used_room_type': last_lodge_Room_type,
            'pms_most_used_room_type': used_room_type_list[0]['_id'][0],
            'pms_total_income': functools.reduce(lambda a, b: a+b, incomes_list),
            'pms_avg_pax': 0,
            'pms_consolidate_nights': functools.reduce(lambda a, b: a+b, nights_list),
            'pms_avg_anticipation': round(statistics.mean(anticipation_list), 2),
            'pms_cancelled_bookings': cancellation_list[0]['count'] if len(cancellation_list)>0 else 0,
            'pms_preferred_sales_channel': sales_channels_list[0]['_id']
        }
            
        return response

    def get_pms_history(customer_id, sensor, skip, limit):
        pass