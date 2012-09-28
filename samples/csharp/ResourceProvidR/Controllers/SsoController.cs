using System.Web.Mvc;

namespace ResourceProvidR.Controllers
{
    public class SsoController : Controller
    {
        public ActionResult Index()
        {
            string resourceName = Request.QueryString["resourceName"];
            string resourceType = Request.QueryString["resourceType"];

            string resourceDisplayName = "";
            if (resourceType.Contains("lightsaber"))
            {
                resourceDisplayName = "LightSaber";
            }
            else
            {
                if (resourceType.Contains("redshirt"))
                {
                    resourceDisplayName = "Red Shirt";
                }
                else
                {
                    resourceDisplayName = "CacheR";
                }
            }

            ViewBag.resourceName = resourceName;
            ViewBag.resourceDisplayName = resourceDisplayName;

            return View();
        }
    }
}
