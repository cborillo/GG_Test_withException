health_receipt_multiple_providers_one_shot = {
    "health_receipts": [
        {
            "provider_info": {
                "provider_registration_number": "12043",
                "provider_first_name": "Pauline",
                "provider_last_name": "Dill",
                "provider_province": "ON",
                "provider_postal_code": "N3T 3J6",
                "provider_phone_number": "844 8573188",
                "under_supervision": True,
            },
            "health_expenses": [
                {
                    "patient_first_name": "Courtney",
                    "date_of_service": "2024-04-15",
                    "service_code": "Psychotherapist",
                    "sub_category_code": "Subsequent",
                    "minutes": 60,
                    "no_of_occur": 1,
                    "phys_reference": False,
                    "total_charge": 203.40,
                }
            ],
        },
        {
            "provider_info": {
                "provider_registration_number": "54321",
                "provider_first_name": "John",
                "provider_last_name": "Doe",
                "provider_province": "BC",
                "provider_postal_code": "V5K 0A1",
                "provider_phone_number": "555 1234567",
                "under_supervision": False,
            },
            "health_expenses": [
                {
                    "patient_first_name": "Alice",
                    "date_of_service": "2024-05-20",
                    "service_code": "Physiotherapist",
                    "sub_category_code": "Initial",
                    "minutes": 45,
                    "no_of_occur": 1,
                    "phys_reference": True,
                    "total_charge": 150.00,
                }
            ],
        },
    ]
}
