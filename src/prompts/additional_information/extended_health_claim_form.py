extended_health_claim_form_page_1_additional_information = """
- For the 'COB' field, it is a checkbox related field. Examine checkboxes left, right or below to the question with the text "Are you, your spouse or dependents covered under any other plan for the expenses being claimed" or equivalent words. Do not mix up with the checkbox of question 'Are these expenses eligible for coverage...'. If there is no checkbox for COB field, set to False.
- For the 'HCSA' field, it is a checkbox related field. Examine checkbox next to the text "check here to use your Health Care Spending Account (HCSA) to reimburse any unpaid portion of this claim" or equivalent words. If the checkbox is checked, set to True, otherwise False. Consider the given checkbox mark is a reliable reference for checkbox value. If there is no checkbox for HCSA (Health Care Spending Account), set to False.
- For the 'HCSA_only' field, it is a checkbox related field. Examine checkbox next to the text "reimburse the eligible expenses directly from my Health Care Spending Account (HCSA)" or equivalent words. If the checkbox is checked, set to True, otherwise False. Consider the given checkbox mark is a reliable reference for checkbox value. If there is no checkbox for HCSA Only, set to False.
- There could be two checkobxes for HCSA and HCSA_only, carefully examine the checkboxes and set the values accordingly. 'HCSA' and 'HCSA_only' fields cannot be both True at the same time.
"""

extended_health_claim_form_page_2_additional_information = """

"""
