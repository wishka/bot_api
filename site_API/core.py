from settings import SiteSettings
from site_API.utils.site_api_handler import SiteApiInterface
site = SiteSettings()


url = "https://weatherapi-com.p.rapidapi.com"
params = {"q": "London", "days": "3"}
headers = {
	"X-RapidAPI-Key": site.api_key,
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com",
}

site_api = SiteApiInterface()


if __name__ == "__main__":
    site_api()