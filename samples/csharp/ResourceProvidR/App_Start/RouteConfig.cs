﻿using System.Web.Mvc;
using System.Web.Routing;

namespace ResourceProvidR
{
    public class RouteConfig
    {
        public static void RegisterRoutes(RouteCollection routes)
        {
            routes.IgnoreRoute("{resource}.axd/{*pathInfo}");

            routes.MapRoute(
                name: "Default",
                url: "Sso/{action}",
                defaults: new { controller = "Sso", action = "Index", id = UrlParameter.Optional }
            );
        }
    }
}