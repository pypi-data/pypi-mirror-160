
LEAD_STATUS = (
    ("assigned", "Assigned"),
    ("in process", "In Process"),
    ("converted", "Converted"),
    ("recycled", "Recycled"),
    ("closed", "Closed"),
)


LEAD_SOURCE = (
    ("call", "Call"),
    ("email", "Email"),
    ("existing customer", "Existing Customer"),
    ("partner", "Partner"),
    ("public relations", "Public Relations"),
    ("compaign", "Campaign"),
    ("other", "Other"),
)

STATUS_CHOICE = (
    ("New", "New"),
    ("Assigned", "Assigned"),
    ("Pending", "Pending"),
    ("Closed", "Closed"),
    ("Rejected", "Rejected"),
    ("Duplicate", "Duplicate"),
)

PRIORITY_CHOICE = (
    ("Low", "Low"),
    ("Normal", "Normal"),
    ("High", "High"),
    ("Urgent", "Urgent"),
)

CASE_TYPE = (("Question", "Question"), ("Incident", "Incident"), ("Problem", "Problem"))

STAGES = (
    ("QUALIFICATION", "QUALIFICATION"),
    ("NEEDS ANALYSIS", "NEEDS ANALYSIS"),
    ("VALUE PROPOSITION", "VALUE PROPOSITION"),
    ("ID.DECISION MAKERS", "ID.DECISION MAKERS"),
    ("PERCEPTION ANALYSIS", "PERCEPTION ANALYSIS"),
    ("PROPOSAL/PRICE QUOTE", "PROPOSAL/PRICE QUOTE"),
    ("NEGOTIATION/REVIEW", "NEGOTIATION/REVIEW"),
    ("CLOSED WON", "CLOSED WON"),
    ("CLOSED LOST", "CLOSED LOST"),
)

SOURCES = (
    ("NONE", "NONE"),
    ("CALL", "CALL"),
    ("EMAIL", " EMAIL"),
    ("EXISTING CUSTOMER", "EXISTING CUSTOMER"),
    ("PARTNER", "PARTNER"),
    ("PUBLIC RELATIONS", "PUBLIC RELATIONS"),
    ("CAMPAIGN", "CAMPAIGN"),
    ("WEBSITE", "WEBSITE"),
    ("OTHER", "OTHER"),
)

BUSINESS_CLIENT_TYPE_CHOICE = (
    ("NONE", "NONE"),
    ("RESELLER", "RESELLER"),
)


