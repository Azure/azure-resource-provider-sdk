using System;
using System.Globalization;
using System.Net;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using System.Web.Http;
using Microsoft.WindowsAzure.CloudServiceManagement.ResourceProviderCommunication;
using ResourceProvidR.Models;

namespace ResourceProvidR.Controllers
{
    public class ResourcesController : ApiController
    {
        //
        // GET /subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}/resources/{resourceName}
        //
        [HttpGet]
        public ResourceOutput GetResource(string subscriptionId, string cloudServiceName, string resourceType, string resourceName)
        {
            if (String.IsNullOrEmpty(cloudServiceName) || String.IsNullOrEmpty(resourceType) || String.IsNullOrEmpty(resourceName))
            {
                throw new HttpResponseException(HttpStatusCode.BadRequest);
            }

            return DataModel.GetResource(subscriptionId, cloudServiceName, resourceName);
        }

        //
        // PUT /subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}/resources/{resourceName}
        //
        [HttpPut]
        public ResourceOutput ProvisionOrUpdateResource(string subscriptionId, string cloudServiceName, string resourceType, string resourceName, ResourceInput resource)
        {
            if (String.IsNullOrEmpty(cloudServiceName) || String.IsNullOrEmpty(resourceType) || String.IsNullOrEmpty(resourceName) || (resource == null))
            {
                throw new HttpResponseException(HttpStatusCode.BadRequest);
            }

            return DataModel.ProvisionOrUpdateResource(subscriptionId, cloudServiceName, resourceType, resourceName, resource);
        }

        //
        // DELETE /subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}/resources/{resourceName}
        //
        [HttpDelete]
        public void DeleteResource(string subscriptionId, string cloudServiceName, string resourceType, string resourceName)
        {
            if (String.IsNullOrEmpty(cloudServiceName) || String.IsNullOrEmpty(resourceType) || String.IsNullOrEmpty(resourceName))
            {
                throw new HttpResponseException(HttpStatusCode.BadRequest);
            }

            DataModel.DeleteResource(subscriptionId, cloudServiceName, resourceName);
        }

        //
        // GET /subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}/resources/{resourceType}/{resourceName}/GenerateSSOToken
        //
        [HttpPost]
        public SsoToken SsoToken(string subscriptionId, string cloudServiceName, string resourceType, string resourceName)
        {
            byte[] theVerySecretKety = UTF8Encoding.UTF32.GetBytes("I do not always use WCF but when I do, I prefer BasicHttpBinding");

            string token = String.Format(CultureInfo.InvariantCulture, "{0}:{1}:{2}", subscriptionId, cloudServiceName, resourceType, resourceName);
            byte[] theHashedData;
            using (HMACSHA1 hmacSha1 = new HMACSHA1())
            {
                theHashedData = hmacSha1.ComputeHash(Encoding.UTF8.GetBytes(token));
            }

            SsoToken theToken = new SsoToken()
            {
                Token = Base32NoPaddingEncode(theHashedData),
                TimeStamp = DateTime.UtcNow.Ticks.ToString()
            };

            return theToken;
        }

        private static string Base32NoPaddingEncode(byte[] data)
        {
            const string base32StandardAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";

            StringBuilder result = new StringBuilder(Math.Max((int)Math.Ceiling(data.Length * 8 / 5.0), 1));

            byte[] emptyBuffer = new byte[] { 0, 0, 0, 0, 0, 0, 0, 0 };
            byte[] workingBuffer = new byte[8];

            // Process input 5 bytes at a time
            for (int i = 0; i < data.Length; i += 5)
            {
                int bytes = Math.Min(data.Length - i, 5);
                Array.Copy(emptyBuffer, workingBuffer, emptyBuffer.Length);
                Array.Copy(data, i, workingBuffer, workingBuffer.Length - (bytes + 1), bytes);
                Array.Reverse(workingBuffer);
                ulong val = BitConverter.ToUInt64(workingBuffer, 0);

                for (int bitOffset = ((bytes + 1) * 8) - 5; bitOffset > 3; bitOffset -= 5)
                {
                    result.Append(base32StandardAlphabet[(int)((val >> bitOffset) & 0x1f)]);
                }
            }

            return result.ToString();
        }       
    }
}
