"""Stream type classes for tap-egencia."""

from __future__ import annotations

from pathlib import Path
import json

from tap_egencia.client import egenciaStream

from singer_sdk import typing as th 

from typing import Any, Dict, Iterable

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class AirTransactionsStream(egenciaStream):
    """Define reporting/transactions stream."""

    name = "air"
    path = "/bi/api/v1/transactions/"
    lob  = "air"
    replication_key = "last_extracted_date"
    reconciled_records_only = False
    schema = th.PropertiesList(
        th.Property("last_extracted_date", th.DateTimeType),
        th.Property("traveler",th.ObjectType(
            th.Property("name", th.StringType),
            th.Property("group", th.StringType),
            th.Property("email", th.StringType),
            th.Property("is_guest", th.StringType),
        )),
        th.Property("point_of_sale_country", th.StringType),
        th.Property("company_name", th.StringType),
        th.Property("department", th.StringType),
        th.Property("transaction_date", th.StringType),
        th.Property("booking_method", th.StringType),
        th.Property("custom_data_fields",th.ObjectType(
            th.Property("Department/Cost Center", th.StringType),
            th.Property("Reason for Travel", th.StringType),
            th.Property("Employee ID", th.StringType),
            th.Property("Testing", th.StringType),
        )),
        th.Property("transaction_type", th.StringType),
        th.Property("advance_purchase_days", th.StringType),
        th.Property("advance_purchase_window", th.StringType),
        th.Property("cabin_class", th.StringType),
        th.Property("class_of_service", th.StringType),
        th.Property("segment_count", th.StringType),
        th.Property("is_active", th.StringType),
        th.Property("purchase_count", th.StringType),
        th.Property("geography_type", th.StringType),
        th.Property("price",th.ObjectType(
            th.Property("base_amount", th.StringType),
            th.Property("taxes", th.StringType),
            th.Property("change_fees", th.StringType),
            th.Property("best_fare_option", th.StringType),
            th.Property("published_fare", th.StringType),
            th.Property("average_leg_amount", th.StringType),
            th.Property("average_segment_amount", th.StringType),
            th.Property("tax_gst", th.StringType),
            th.Property("tax_hst", th.StringType),
            th.Property("tax_qst", th.StringType),
            th.Property("true_ticket_amount", th.StringType),
        )),
        th.Property("duration",th.ObjectType(
            th.Property("minutes", th.StringType),
        )),
        th.Property("identifier",th.ObjectType(
            th.Property("itinerary_number", th.StringType),
            th.Property("record_locator", th.StringType),
            th.Property("confirmation_number", th.StringType),
            th.Property("invoice_number", th.StringType),
        )),
        th.Property("policy",th.ObjectType(
            th.Property("in_policy", th.StringType),
            th.Property("policy_reason_code", th.StringType),
            th.Property("policy_reason_description", th.StringType),
        )),
        th.Property("ticket_code", th.StringType),
        th.Property("client_code", th.StringType),
        th.Property("travel_dates",th.ObjectType(
            th.Property("travel_start_date", th.StringType),
            th.Property("travel_end_date", th.StringType),
        )),
        th.Property("ticketing_airline", th.StringType),
        th.Property("fare_type", th.StringType),
        th.Property("leg_count", th.StringType),
        th.Property("fractional_ticket_count", th.StringType),
        th.Property("route", th.StringType),
        th.Property("distance",th.ObjectType(
            th.Property("km", th.StringType),
            th.Property("miles", th.StringType),
        )),
        th.Property("booking_date", th.StringType),
        th.Property("is_sat_night_stay", th.StringType),
        th.Property("original_ticket_code", th.StringType),
        th.Property("fare_basis_code", th.StringType),
        th.Property("origin_destination_info",th.ObjectType(
            th.Property("origin_country", th.StringType),
            th.Property("destination_country", th.StringType),
            th.Property("origin_region", th.StringType),
            th.Property("destination_region", th.StringType),
            th.Property("origin_airport_code", th.StringType),
            th.Property("destination_airport_code", th.StringType),
            th.Property("origin_airport", th.StringType),
            th.Property("destination_airport", th.StringType),
            th.Property("airport_code_pair_alphabetical", th.StringType),
            th.Property("airport_location_pair_alphabetical", th.StringType),
            th.Property("airport1_alphabetical", th.StringType),
            th.Property("airport2_alphabetical", th.StringType),
            th.Property("airport1_code_alphabetical", th.StringType),
            th.Property("airport2_code_alphabetical", th.StringType),
            th.Property("airport1_location_alphabetical", th.StringType),
            th.Property("airport2_location_alphabetical", th.StringType),
            th.Property("origin_location", th.StringType),
            th.Property("destination_location", th.StringType),
            th.Property("airport1_country_alphabetical", th.StringType),
            th.Property("airport2_country_alphabetical", th.StringType),
            th.Property("origin_and_destination_airport_codes", th.StringType),
            th.Property("origin_and_destination_locations", th.StringType),
        )),
        th.Property("carrier_code", th.StringType),
        th.Property("trip_geometry", th.StringType),
        th.Property("low_cost_carrier", th.StringType),
        th.Property("ticket_count", th.StringType),
        th.Property("booker", th.ObjectType(
            th.Property("name", th.StringType),
            th.Property("role", th.StringType),
        )),
        th.Property("point_of_sale_type", th.StringType),
        th.Property("parent_client_code", th.StringType),
        th.Property("airline_alliance", th.StringType),
        th.Property("approval", th.BooleanType),
        th.Property("ndc", th.BooleanType),
        th.Property("co2",th.ArrayType(th.ObjectType(
            th.Property("kg", th.StringType),
            th.Property("lbs", th.StringType),
            th.Property("carbon_emission_kg", th.StringType),
            th.Property("carbon_emission_lbs", th.StringType),
            th.Property("coefficient_year", th.StringType),
        ))),
        th.Property("savings",th.ObjectType(
            th.Property("egencia_preferred_rate_savings", th.StringType),
            th.Property("negotiated_savings", th.StringType),
            th.Property("savings_over_published_fare", th.StringType),
            th.Property("missed_savings", th.StringType),
        )),
    ).to_dict()

class ReconciledAirTransactionsStream(egenciaStream):
    """Define reporting/transactions stream."""

    name = "reconciled_air"
    path = "/bi/api/v1/transactions/"
    lob  = "air"
    replication_key = "last_extracted_date"
    reconciled_records_only = True
    schema = th.PropertiesList(
        th.Property("last_extracted_date", th.DateTimeType),
        th.Property("traveler",th.ObjectType(
            th.Property("name", th.StringType),
            th.Property("group", th.StringType),
            th.Property("email", th.StringType),
            th.Property("is_guest", th.StringType),
        )),
        th.Property("point_of_sale_country", th.StringType),
        th.Property("company_name", th.StringType),
        th.Property("department", th.StringType),
        th.Property("transaction_date", th.StringType),
        th.Property("booking_method", th.StringType),
        th.Property("custom_data_fields",th.ObjectType(
            th.Property("Department/Cost Center", th.StringType),
            th.Property("Reason for Travel", th.StringType),
            th.Property("Employee ID", th.StringType),
            th.Property("Testing", th.StringType),
        )),
        th.Property("transaction_type", th.StringType),
        th.Property("advance_purchase_days", th.StringType),
        th.Property("advance_purchase_window", th.StringType),
        th.Property("cabin_class", th.StringType),
        th.Property("class_of_service", th.StringType),
        th.Property("segment_count", th.StringType),
        th.Property("is_active", th.StringType),
        th.Property("purchase_count", th.StringType),
        th.Property("geography_type", th.StringType),
        th.Property("price",th.ObjectType(
            th.Property("base_amount", th.StringType),
            th.Property("taxes", th.StringType),
            th.Property("change_fees", th.StringType),
            th.Property("best_fare_option", th.StringType),
            th.Property("published_fare", th.StringType),
            th.Property("average_leg_amount", th.StringType),
            th.Property("average_segment_amount", th.StringType),
            th.Property("tax_gst", th.StringType),
            th.Property("tax_hst", th.StringType),
            th.Property("tax_qst", th.StringType),
            th.Property("true_ticket_amount", th.StringType),
        )),
        th.Property("duration",th.ObjectType(
            th.Property("minutes", th.StringType),
        )),
        th.Property("identifier",th.ObjectType(
            th.Property("itinerary_number", th.StringType),
            th.Property("record_locator", th.StringType),
            th.Property("confirmation_number", th.StringType),
            th.Property("invoice_number", th.StringType),
        )),
        th.Property("policy",th.ObjectType(
            th.Property("in_policy", th.StringType),
            th.Property("policy_reason_code", th.StringType),
            th.Property("policy_reason_description", th.StringType),
        )),
        th.Property("ticket_code", th.StringType),
        th.Property("client_code", th.StringType),
        th.Property("travel_dates",th.ObjectType(
            th.Property("travel_start_date", th.StringType),
            th.Property("travel_end_date", th.StringType),
        )),
        th.Property("ticketing_airline", th.StringType),
        th.Property("fare_type", th.StringType),
        th.Property("leg_count", th.StringType),
        th.Property("fractional_ticket_count", th.StringType),
        th.Property("route", th.StringType),
        th.Property("distance",th.ObjectType(
            th.Property("km", th.StringType),
            th.Property("miles", th.StringType),
        )),
        th.Property("booking_date", th.StringType),
        th.Property("is_sat_night_stay", th.StringType),
        th.Property("original_ticket_code", th.StringType),
        th.Property("fare_basis_code", th.StringType),
        th.Property("origin_destination_info",th.ObjectType(
            th.Property("origin_country", th.StringType),
            th.Property("destination_country", th.StringType),
            th.Property("origin_region", th.StringType),
            th.Property("destination_region", th.StringType),
            th.Property("origin_airport_code", th.StringType),
            th.Property("destination_airport_code", th.StringType),
            th.Property("origin_airport", th.StringType),
            th.Property("destination_airport", th.StringType),
            th.Property("airport_code_pair_alphabetical", th.StringType),
            th.Property("airport_location_pair_alphabetical", th.StringType),
            th.Property("airport1_alphabetical", th.StringType),
            th.Property("airport2_alphabetical", th.StringType),
            th.Property("airport1_code_alphabetical", th.StringType),
            th.Property("airport2_code_alphabetical", th.StringType),
            th.Property("airport1_location_alphabetical", th.StringType),
            th.Property("airport2_location_alphabetical", th.StringType),
            th.Property("origin_location", th.StringType),
            th.Property("destination_location", th.StringType),
            th.Property("airport1_country_alphabetical", th.StringType),
            th.Property("airport2_country_alphabetical", th.StringType),
            th.Property("origin_and_destination_airport_codes", th.StringType),
            th.Property("origin_and_destination_locations", th.StringType),
        )),
        th.Property("carrier_code", th.StringType),
        th.Property("trip_geometry", th.StringType),
        th.Property("low_cost_carrier", th.StringType),
        th.Property("ticket_count", th.StringType),
        th.Property("booker", th.ObjectType(
            th.Property("name", th.StringType),
            th.Property("role", th.StringType),
        )),
        th.Property("point_of_sale_type", th.StringType),
        th.Property("parent_client_code", th.StringType),
        th.Property("airline_alliance", th.StringType),
        th.Property("approval", th.BooleanType),
        th.Property("ndc", th.BooleanType),
        th.Property("co2",th.ArrayType(th.ObjectType(
            th.Property("kg", th.StringType),
            th.Property("lbs", th.StringType),
            th.Property("carbon_emission_kg", th.StringType),
            th.Property("carbon_emission_lbs", th.StringType),
            th.Property("coefficient_year", th.StringType),
        ))),
        th.Property("savings",th.ObjectType(
            th.Property("egencia_preferred_rate_savings", th.StringType),
            th.Property("negotiated_savings", th.StringType),
            th.Property("savings_over_published_fare", th.StringType),
            th.Property("missed_savings", th.StringType),
        )),
    ).to_dict()


class HotelTransactionsStream(egenciaStream):
    """Define reporting/transactions stream."""

    name = "hotel"
    path = "/bi/api/v1/transactions/"
    lob  = "hotel"
    replication_key = "last_extracted_date"
    reconciled_records_only = False
    schema = th.PropertiesList(
        th.Property("last_extracted_date", th.DateTimeType),
        th.Property("address",th.ObjectType(
            th.Property("address_line1", th.StringType),
            th.Property("city", th.StringType),
            th.Property("country", th.StringType),
            th.Property("postal_code", th.StringType),
            th.Property("province", th.StringType),
            th.Property("region", th.StringType),
        )),
        th.Property("booking_date", th.StringType),
        th.Property("point_of_sale_country", th.StringType),
        th.Property("advance_purchase_days", th.StringType),
        th.Property("company_name", th.StringType),
        th.Property("custom_data_fields",th.ObjectType(
            th.Property("Department/Cost Center", th.StringType),
            th.Property("Reason for Travel", th.StringType),
            th.Property("Employee ID", th.StringType),
            th.Property("Testing", th.StringType),
        )),
        th.Property("department", th.StringType),
        th.Property("geography_type", th.StringType),
        th.Property("is_active", th.StringType),
        th.Property("hotel_brand_name", th.StringType),
        th.Property("hotel_brand", th.StringType),
        th.Property("hotel_chain_name", th.StringType),
        th.Property("hotel_chain", th.StringType),
        th.Property("hotel_name", th.StringType),
        th.Property("hotel_country_code", th.StringType),
        th.Property("hotel_city_code", th.StringType),
        th.Property("hotel_airport_code", th.StringType),
        th.Property("hotel_night_rate", th.StringType),
        th.Property("credit_card_type", th.StringType),
        th.Property("hotel_room_count", th.StringType),
        th.Property("room_count", th.StringType),
        th.Property("lowest_published_rate", th.StringType),
        th.Property("hotel_nights", th.StringType),
        th.Property("hotel_savings", th.StringType),
        th.Property("savings",th.ObjectType(
            th.Property("savings_over_published_rate", th.StringType),
            th.Property("dynamic_rate_cap_savings", th.StringType),
        )),
        th.Property("parent_client_code", th.StringType),
        th.Property("hotel_chain_code", th.StringType),
        th.Property("identifier",th.ObjectType(
            th.Property("confirmation_number", th.StringType),
            th.Property("itinerary_number", th.StringType),
            th.Property("record_locator", th.StringType),
            th.Property("invoice_number", th.StringType),
        )),
        th.Property("booking_method", th.StringType),
        th.Property("is_special_request", th.StringType),
        th.Property("phone_number_fax", th.StringType),
        th.Property("phone_number_local", th.StringType),
        th.Property("booker", th.ObjectType(
            th.Property("name", th.StringType),
            th.Property("role", th.StringType),
        )),
        th.Property("point_of_sale_type", th.StringType),
        th.Property("invoice_date", th.StringType),
        th.Property("duration",th.ObjectType(
            th.Property("minutes", th.StringType),
        )),
        th.Property("client_code", th.StringType),
        th.Property("approval", th.StringType),
        th.Property("is_non_standard_booking", th.StringType),
        th.Property("dynamic_hotel_rate_cap", th.StringType),
        th.Property("policy",th.ObjectType(
            th.Property("in_policy", th.StringType),
            th.Property("policy_reason_code", th.StringType),
            th.Property("policy_reason_description", th.StringType),
        )),
        th.Property("price",th.ObjectType(
            th.Property("base", th.StringType),
            th.Property("base_amount", th.StringType),
            th.Property("change_fee_amount", th.StringType),
            th.Property("change_fee", th.StringType),
            th.Property("coupon_amount", th.StringType),
            th.Property("extra_person_amount", th.StringType),
            th.Property("extra_guest_charges", th.StringType),
            th.Property("fee", th.StringType),
            th.Property("fees", th.StringType),
            th.Property("goodwill_amount", th.StringType),
            th.Property("tax", th.StringType),
            th.Property("taxes", th.StringType),
            th.Property("total", th.StringType),
            th.Property("transaction_amount", th.StringType),
        )),
        th.Property("rate_type", th.StringType),
        th.Property("advance_purchase_window", th.StringType),
        th.Property("purchase_count", th.StringType),
        th.Property("transaction_date", th.StringType),
        th.Property("co2",th.ArrayType(th.ObjectType(
            th.Property("carbon_emission_kg", th.StringType),
            th.Property("carbon_emission_lbs", th.StringType),
            th.Property("coefficient", th.StringType),
        ))),
        th.Property("transaction_type", th.StringType),
        th.Property("travel_dates",th.ObjectType(
            th.Property("travel_end_date", th.StringType),
            th.Property("travel_start_date", th.StringType),
        )),
        th.Property("traveler",th.ObjectType(
            th.Property("email", th.StringType),
            th.Property("group", th.StringType),
            th.Property("is_guest", th.StringType),
            th.Property("name", th.StringType),
        )),
    ).to_dict()




class TrainTransactionsStream(egenciaStream):
    """Define reporting/transactions stream."""

    name = "train"
    path = "/bi/api/v1/transactions/"
    lob  = "train"
    replication_key = "last_extracted_date"
    reconciled_records_only = False
    schema = th.PropertiesList(
        th.Property("last_extracted_date", th.DateTimeType),
        th.Property("advance_purchase_days", th.StringType),
        th.Property("advance_purchase_window", th.StringType),
        th.Property("point_of_sale_country", th.StringType),
        th.Property("arrival_date_time", th.StringType),
        th.Property("booking_method", th.StringType),
        th.Property("cabin_class", th.StringType),
        th.Property("carrier", th.StringType),
        th.Property("class_of_service", th.StringType),
        th.Property("company_name", th.StringType),
        th.Property("client_code", th.StringType),
        th.Property("parent_client_code", th.StringType),
        th.Property("corporate_travel_group", th.StringType),
        th.Property("co2",th.ArrayType(th.ObjectType(
            th.Property("carbon_emission_kg", th.StringType),
            th.Property("carbon_emission_lbs", th.StringType),
        ))),
        th.Property("custom_data_fields",th.ObjectType(
            th.Property("Department/Cost Center", th.StringType),
            th.Property("Reason for Travel", th.StringType),
            th.Property("Employee ID", th.StringType),
            th.Property("Testing", th.StringType),
        )),
        th.Property("department", th.StringType),
        th.Property("departure_date_time", th.StringType),
        th.Property("travel_dates",th.ObjectType(
            th.Property("travel_end_date", th.StringType),
            th.Property("travel_start_date", th.StringType),
        )),
        th.Property("distance",th.ObjectType(
            th.Property("km", th.StringType),
            th.Property("miles", th.StringType),
        )),
        th.Property("fare_type", th.StringType),
        th.Property("geography_type", th.StringType),
        th.Property("identifier",th.ObjectType(
            th.Property("invoice_number", th.StringType),
            th.Property("record_locator", th.StringType),
            th.Property("itinerary_number", th.StringType),
        )),
        th.Property("invoice_date", th.StringType),
        th.Property("is_sat_night_stay", th.StringType),
        th.Property("leg_info",th.ObjectType(
            th.Property("average_segment_amount", th.StringType),
            th.Property("cabin_class", th.StringType),
            th.Property("carrier", th.StringType),
            th.Property("class_of_service", th.StringType),
            th.Property("geography_type", th.StringType),
            th.Property("is_active", th.StringType),
            th.Property("origin_destination_info",th.ObjectType(
                th.Property("origin_and_destination_station_codes", th.StringType),
                th.Property("station_code_pair_alphabetical", th.StringType),
                th.Property("origin_and_destination_station_locations", th.StringType),
                th.Property("station_location_pair_alphabetical", th.StringType),
                th.Property("origin_location", th.StringType),
                th.Property("destination_location", th.StringType),
                th.Property("origin_country", th.StringType),
                th.Property("destination_country", th.StringType),
                th.Property("station2_country_alphabetical", th.StringType),
                th.Property("station1_location_alphabetical", th.StringType),
                th.Property("station2_location_alphabetical", th.StringType),
                th.Property("destination_station", th.StringType),
                th.Property("station2_alphabetical", th.StringType),
                th.Property("destination_station_code", th.StringType),
                th.Property("station2_code_alphabetical", th.StringType),
                th.Property("station1_country_alphabetical", th.StringType),
                th.Property("origin_station", th.StringType),
                th.Property("station1_alphabetical", th.StringType),
                th.Property("origin_station_code", th.StringType),
                th.Property("station1_code_alphabetical", th.StringType),
            )),
        )),
        th.Property("origin_destination_info",th.ObjectType(
            th.Property("origin_and_destination_station_codes", th.StringType),
            th.Property("station_code_pair_alphabetical", th.StringType),
            th.Property("origin_and_destination_station_locations", th.StringType),
            th.Property("station_location_pair_alphabetical", th.StringType),
            th.Property("origin_country", th.StringType),
            th.Property("destination_country", th.StringType),
            th.Property("station2_country_alphabetical", th.StringType),
            th.Property("origin_location", th.StringType),
            th.Property("destination_location", th.StringType),
            th.Property("station1_location_alphabetical", th.StringType),
            th.Property("station2_location_alphabetical", th.StringType),
            th.Property("destination_station", th.StringType),
            th.Property("station2_alphabetical", th.StringType),
            th.Property("destination_station_code", th.StringType),
            th.Property("station2_code_alphabetical", th.StringType),
            th.Property("station1_country_alphabetical", th.StringType),
            th.Property("origin_station", th.StringType),
            th.Property("station1_alphabetical", th.StringType),
            th.Property("origin_station_code", th.StringType),
            th.Property("station1_code_alphabetical", th.StringType),
        )),
        th.Property("leg_number", th.StringType),
        th.Property("policy",th.ObjectType(
            th.Property("in_policy", th.StringType),
            th.Property("policy_reason_code", th.StringType),
            th.Property("policy_reason_description", th.StringType),
        )),
        th.Property("price",th.ObjectType(
            th.Property("leg_amount", th.StringType),
            th.Property("trip_amount", th.StringType),
            th.Property("transaction_amount", th.StringType),
            th.Property("base_amount", th.StringType),
            th.Property("taxes", th.StringType),
            th.Property("average_leg_amount", th.StringType),
            th.Property("average_segment_amount", th.StringType),
        )),
        th.Property("routing", th.StringType),
        th.Property("ticket_code", th.StringType),
        th.Property("original_ticket_code", th.StringType),
        th.Property("transaction_date", th.StringType),
        th.Property("booker", th.ObjectType(
            th.Property("name", th.StringType),
            th.Property("role", th.StringType),
        )),
        th.Property("is_special_request", th.StringType),
        th.Property("is_active", th.StringType),
        th.Property("purchase_count", th.StringType),
        th.Property("duration",th.ObjectType(
            th.Property("minutes", th.StringType),
        )),
        th.Property("leg_count", th.StringType),
        th.Property("booking_date", th.StringType),
        th.Property("ticketing_fare_type", th.StringType),
        th.Property("ticket_count", th.StringType),
        th.Property("fraction_ticket_count", th.StringType),
        th.Property("carrier_code", th.StringType),
        th.Property("approval", th.StringType),
        th.Property("traveler",th.ObjectType(
            th.Property("email", th.StringType),
            th.Property("is_guest", th.StringType),
            th.Property("name", th.StringType),
            th.Property("group", th.StringType),
        )),
        th.Property("trip_geometry", th.StringType),
        th.Property("segment_amount_average", th.StringType),
        th.Property("segment_count", th.StringType),
    ).to_dict()


class CarTransactionsStream(egenciaStream):
    """Define reporting/transactions stream."""

    name = "car"
    path = "/bi/api/v1/transactions/"
    lob  = "car"
    replication_key = "last_extracted_date"
    reconciled_records_only = False
    schema = th.PropertiesList(
        th.Property("last_extracted_date", th.DateTimeType),
    	th.Property("company_name", th.StringType),
        th.Property("custom_data_fields",th.ObjectType(
            th.Property("Department/Cost Center", th.StringType),
            th.Property("Reason for Travel", th.StringType),
            th.Property("Employee ID", th.StringType),
            th.Property("Testing", th.StringType),
        )),
        th.Property("car_daily_rate", th.StringType),
        th.Property("car_chain_code", th.StringType),
        th.Property("car_display_group_id", th.StringType),
        th.Property("car_display_group_name", th.StringType),
        th.Property("total_rental_days", th.StringType),
        th.Property("rental_days", th.StringType),
        th.Property("client_code", th.StringType),
        th.Property("is_active", th.StringType),
        th.Property("booking_date", th.StringType),
        th.Property("parent_client_code", th.StringType),
        th.Property("acriss_code", th.StringType),
        th.Property("department", th.StringType),
        th.Property("drop_off_airport", th.StringType),
        th.Property("drop_off_city", th.StringType),
        th.Property("travel_dates",th.ObjectType(
            th.Property("travel_end_date", th.StringType),
            th.Property("travel_start_date", th.StringType),
        )),
        th.Property("booker", th.ObjectType(
            th.Property("name", th.StringType),
            th.Property("role", th.StringType),
        )),
        th.Property("geography_type", th.StringType),
        th.Property("identifier",th.ObjectType(
            th.Property("confirmation_number", th.StringType),
            th.Property("itinerary_number", th.StringType),
            th.Property("record_locator", th.StringType),
        )),
        th.Property("booking_method", th.StringType),
        th.Property("is_collected", th.StringType),
        th.Property("is_delivered", th.StringType),
        th.Property("is_hired_car", th.StringType),
        th.Property("is_online_booking", th.StringType),
        th.Property("is_special_request", th.StringType),
        th.Property("advance_purchase_days", th.StringType),
        th.Property("advance_purchase_window", th.StringType),
        th.Property("payment_method", th.StringType),
        th.Property("pick_up_airport", th.StringType),
        th.Property("pick_up_city", th.StringType),
        th.Property("pick_up_country", th.StringType),
        th.Property("point_of_sale_country", th.StringType),
        th.Property("vendor", th.StringType),
        th.Property("purchase_count", th.StringType),
        th.Property("duration",th.ObjectType(
            th.Property("minutes", th.StringType),
        )),
        th.Property("reservation_count", th.StringType),
        th.Property("vendor_code", th.StringType),
        th.Property("car_type", th.StringType),
        th.Property("origin_destination_info", th.ObjectType(
            th.Property("pick_up_city", th.StringType),
            th.Property("drop_off_city", th.StringType),
            th.Property("pick_up_airport", th.StringType),
            th.Property("drop_off_airport", th.StringType),
            th.Property("pick_up_country", th.StringType),
        )),
        th.Property("approval", th.BooleanType),
        th.Property("policy",th.ObjectType(
            th.Property("in_policy", th.StringType),
            th.Property("policy_reason_code", th.StringType),
            th.Property("policy_reason_description", th.StringType),
        )),
        th.Property("price",th.ObjectType(
            th.Property("base_amount", th.StringType),
            th.Property("fees", th.StringType),
            th.Property("taxes", th.StringType),
            th.Property("transaction_amount", th.StringType),
            th.Property("taxes_and_fees", th.StringType),
        )),
        th.Property("rate_type", th.StringType),
        th.Property("reservations", th.StringType),
        th.Property("transaction_date", th.StringType),
        th.Property("transaction_type", th.StringType),
        th.Property("traveler",th.ObjectType(
            th.Property("email", th.StringType),
            th.Property("group", th.StringType),
            th.Property("is_guest", th.StringType),
            th.Property("name", th.StringType),
        )),
        th.Property("vendor_name", th.StringType),
    ).to_dict()

class GroundTransactionsStream(egenciaStream):
    """Define reporting/transactions stream.
    NO ACCESS ATM
    """

    name = "ground"
    path = "/bi/api/v1/transactions/"
    lob  = "ground"
    replication_key = "last_extracted_date"
    reconciled_records_only = False
    schema = th.PropertiesList(
        th.Property("last_extracted_date", th.DateTimeType),
        th.Property("company_name", th.StringType),
        th.Property("custom_data_fields",th.ObjectType(
            th.Property("Department/Cost Center", th.StringType),
            th.Property("Reason for Travel", th.StringType),
            th.Property("Employee ID", th.StringType),
            th.Property("Testing", th.StringType),
        )),
        th.Property("passenger_count", th.StringType),
        th.Property("miles", th.StringType),
        th.Property("km", th.StringType),
        th.Property("booking_menthod", th.StringType),
        th.Property("pick_up_location_type", th.StringType),
        th.Property("drop_off_location_type", th.StringType),
        th.Property("pick_up_region", th.StringType),
        th.Property("drop_off_region", th.StringType),
        th.Property("client_code", th.StringType),
        th.Property("parent_client_code", th.StringType),
        th.Property("booking_date", th.StringType),
        th.Property("department", th.StringType),
        th.Property("drop_off_airport", th.StringType),
        th.Property("drop_off_city", th.StringType),
        th.Property("duration",th.ObjectType(
            th.Property("minutes", th.StringType),
        )),
        th.Property("vehicle",th.ObjectType(
            th.Property("type", th.StringType),
            th.Property("category", th.StringType),
        )),
        th.Property("geography_type", th.StringType),
        th.Property("identifier",th.ObjectType(
            th.Property("confirmation_number", th.StringType),
            th.Property("record_locator", th.StringType),
        )),
        th.Property("cancellation_rule", th.StringType),
        th.Property("pick_up_street", th.StringType),
        th.Property("drop_off_street", th.StringType),
        th.Property("transfer_type", th.StringType),
        th.Property("is_special_request", th.StringType),
        th.Property("advance_purchase_days", th.StringType),
        th.Property("advance_purchase_window", th.StringType),
        th.Property("pick_up_airport", th.StringType),
        th.Property("pick_up_city", th.StringType),
        th.Property("pick_up_country", th.StringType),
        th.Property("drop_off_country", th.StringType),
        th.Property("price",th.ObjectType(
            th.Property("base", th.StringType),
            th.Property("tax", th.StringType),
            th.Property("total", th.StringType),
            th.Property("transaction_amount", th.StringType),
        )),
        th.Property("reservation_count", th.StringType),
        th.Property("transaction_date", th.StringType),
        th.Property("is_active", th.StringType),
        th.Property("transaction_type", th.StringType),
        th.Property("traveler",th.ObjectType(
            th.Property("email", th.StringType),
            th.Property("is_guest", th.StringType),
            th.Property("name", th.StringType),
        )),
        th.Property("vendor_name", th.StringType),
    ).to_dict()


class FeeTransactionsStream(egenciaStream):
    """Define reporting/transactions stream."""

    name = "fee"
    path = "/bi/api/v1/transactions/"
    lob  = "fees"
    replication_key = "last_extracted_date"
    reconciled_records_only = False
    schema = th.PropertiesList(
        th.Property("last_extracted_date", th.DateTimeType),
        th.Property("company_name", th.StringType),
        th.Property("custom_data_fields",th.ObjectType(
            th.Property("Department/Cost Center", th.StringType),
            th.Property("Reason for Travel", th.StringType),
            th.Property("Employee ID", th.StringType),
            th.Property("Testing", th.StringType),
        )),
        th.Property("department", th.StringType),
        th.Property("identifier",th.ObjectType(
            th.Property("confirmation_number", th.StringType),
            th.Property("itinerary_number", th.StringType),
            th.Property("record_locator", th.StringType),
            th.Property("invoice_number", th.StringType),
        )),
        th.Property("approval", th.StringType),
        th.Property("booking_method", th.StringType),
        th.Property("booking_category", th.StringType),
        th.Property("ticket_count", th.StringType),
        th.Property("transaction_type", th.StringType),
        th.Property("invoice_number", th.StringType),
        th.Property("fee_category", th.StringType),
        th.Property("is_active", th.StringType),
        th.Property("meeting_name", th.StringType),
        th.Property("fee_service_type", th.StringType),
        th.Property("feetype", th.StringType),
        th.Property("client_code", th.StringType),
        th.Property("parent_client_code", th.StringType),
        th.Property("line_of_business", th.StringType),
        th.Property("point_of_sale_country", th.StringType),
        th.Property("invoice_date", th.StringType),
        th.Property("purchase_count", th.StringType),
        th.Property("geography_type", th.StringType),
        th.Property("policy",th.ObjectType(
            th.Property("in_policy", th.StringType),
            th.Property("policy_reason_code", th.StringType),
            th.Property("policy_reason_description", th.StringType),
        )),
        th.Property("ticket_code", th.StringType),
        th.Property("travel_dates",th.ObjectType(
            th.Property("travel_end_date", th.StringType),
            th.Property("travel_start_date", th.StringType),
        )),
        th.Property("fee_type", th.StringType),
        th.Property("fee_count", th.StringType),
        th.Property("is_waived", th.StringType),
        th.Property("waived_amount", th.StringType),
        th.Property("trip_id", th.StringType),
        th.Property("trip_name", th.StringType),
        th.Property("price",th.ObjectType(
            th.Property("base_amount", th.StringType),
            th.Property("fees", th.StringType),
            th.Property("taxes", th.StringType),
            th.Property("transaction_amount_vat", th.StringType),
            th.Property("transaction_amount_gst", th.StringType),
            th.Property("transaction_amount_hst", th.StringType),
            th.Property("transaction_amount_qst", th.StringType),
            th.Property("transaction_amount", th.StringType),
            th.Property("tax_vat", th.StringType),
            th.Property("tax_gst", th.StringType),
            th.Property("tax_hst", th.StringType),
            th.Property("tax_qst", th.StringType),
        )),
        th.Property("transaction_date", th.StringType),
        th.Property("traveler",th.ObjectType(
            th.Property("email", th.StringType),
            th.Property("group", th.StringType),
            th.Property("is_guest", th.StringType),
            th.Property("name", th.StringType),
            th.Property("meeting_attendee_group", th.StringType),
        )),
    ).to_dict()
