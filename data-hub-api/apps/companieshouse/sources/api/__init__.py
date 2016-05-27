import slumber

from django.conf import settings

api = slumber.API(
    "https://api.companieshouse.gov.uk/",
    auth=(
        settings.COMPANIES_HOUSE_TOKEN, ""
    )
)
