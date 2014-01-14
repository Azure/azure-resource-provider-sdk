#Resource Operation: Delete Resource
A user can delete a Resource from the [Management Portal](https://manage.microsoft.com). When this happens, Windows Azure will severe the billing relationship and ask your RP to delete the resource.

##Request
URL: `https://<base_uri>/subscriptions/cloudservices/<cloud_service_name>/resources/<resource_type>/<resource_name>`

Method: `DELETE`

##Response
- Your RP should return `200` or `201` on a successful `DELETE` on a Resource.
- If the Resource does not exist, return `404`. Windows Azure will not retry the delete operation.
- An HTTP status code in the `5xx` range indicates that a timeout or error occurred in your service. Windows Azure will retry the operation.
- If Windows Azure receives any other HTTP status code, it will not retry the operation.