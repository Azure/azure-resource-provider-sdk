using System.Threading.Tasks;
using System.Web.Http;
using Microsoft.WindowsAzure.CloudServiceManagement.ResourceProviderCommunication;

namespace ResourceProvidR.Controllers
{
    public class EventsController : ApiController
    {
        //
        // POST /events
        //
        [HttpPost]
        public void HandleSubscriptionNotifications(EntityEvent entity)
        {
        }
    }
}