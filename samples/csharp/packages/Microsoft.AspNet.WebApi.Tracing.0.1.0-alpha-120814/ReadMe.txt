Microsoft ASP.NET Web API Tracing
=================================

This package allows the ASP.NET Web API framework to trace to System.Diagnostics.Trace.
 
In addition to installing the necessary package dependencies, the following
source file was added to your project:

    App_Start\TraceConfig.cs

To enable tracing in your application, please add the following line of code
to your startup code (WebApiConfig.cs or Global.asax.cs in an MVC 4 project):

    TraceConfig.Register(config);

where 'config' is the HttpConfiguration instance for your application.

For additional information on debugging and tracing in ASP.NET Web API, refer to:
    http://www.asp.net/web-api
