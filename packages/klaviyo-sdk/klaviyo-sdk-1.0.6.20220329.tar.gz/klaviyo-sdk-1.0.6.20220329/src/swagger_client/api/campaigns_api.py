# coding: utf-8

"""
    Klaviyo API

    Empowering creators to own their destiny  # noqa: E501

    OpenAPI spec version: 2022.03.29
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from swagger_client.api_client import ApiClient


class CampaignsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.warned = []

    def cancel_campaign(self, campaign_id, **kwargs):  # noqa: E501
        """Cancel a Campaign  # noqa: E501

        Cancels a campaign send. Marks a campaign as cancelled regardless of it's current status.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.cancel_campaign(campaign_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str campaign_id: (required)
        :return: Campaign
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.cancel_campaign_with_http_info(campaign_id, **kwargs)  # noqa: E501
        else:
            (data) = self.cancel_campaign_with_http_info(campaign_id, **kwargs)  # noqa: E501
            return data

    def cancel_campaign_with_http_info(self, campaign_id, **kwargs):  # noqa: E501
        """Cancel a Campaign  # noqa: E501

        Cancels a campaign send. Marks a campaign as cancelled regardless of it's current status.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.cancel_campaign_with_http_info(campaign_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str campaign_id: (required)
        :return: Campaign
                 If the method is called asynchronously,
                 returns the request thread.
        """


        all_params = ['campaign_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method cancel_campaign" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'campaign_id' is set
        if ('campaign_id' not in params or
                params['campaign_id'] is None):
            raise ValueError("Missing the required parameter `campaign_id` when calling `cancel_campaign`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'campaign_id' in params:
            path_params['campaign_id'] = params['campaign_id']  # noqa: E501

        query_params = []

        header_params = {}


        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKeyAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v1/campaign/{campaign_id}/cancel', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Campaign',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def clone_campaign(self, campaign_id, **kwargs):  # noqa: E501
        """Clone a Campaign  # noqa: E501

        Creates a copy of a campaign. The new campaign starts as a draft.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clone_campaign(campaign_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str campaign_id: (required)
        :param str name:
        :param str list_id:
        :return: Campaign
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.clone_campaign_with_http_info(campaign_id, **kwargs)  # noqa: E501
        else:
            (data) = self.clone_campaign_with_http_info(campaign_id, **kwargs)  # noqa: E501
            return data

    def clone_campaign_with_http_info(self, campaign_id, **kwargs):  # noqa: E501
        """Clone a Campaign  # noqa: E501

        Creates a copy of a campaign. The new campaign starts as a draft.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clone_campaign_with_http_info(campaign_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str campaign_id: (required)
        :param str name:
        :param str list_id:
        :return: Campaign
                 If the method is called asynchronously,
                 returns the request thread.
        """


        all_params = ['campaign_id', 'name', 'list_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method clone_campaign" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'campaign_id' is set
        if ('campaign_id' not in params or
                params['campaign_id'] is None):
            raise ValueError("Missing the required parameter `campaign_id` when calling `clone_campaign`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'campaign_id' in params:
            path_params['campaign_id'] = params['campaign_id']  # noqa: E501

        query_params = []

        header_params = {}


        form_params = []
        local_var_files = {}
        if 'name' in params:
            form_params.append(('name', params['name']))  # noqa: E501
        if 'list_id' in params:
            form_params.append(('list_id', params['list_id']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKeyAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v1/campaign/{campaign_id}/clone', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Campaign',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_campaign(self, **kwargs):  # noqa: E501
        """Create New Campaign  # noqa: E501

        Creates a new campaign. The created campaign is a draft and is not automatically sent.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_campaign(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str list_id:
        :param str template_id:
        :param str from_email:
        :param str from_name:
        :param str subject:
        :param str name:
        :param bool use_smart_sending:
        :param bool add_google_analytics:
        :return: Campaign
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_campaign_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.create_campaign_with_http_info(**kwargs)  # noqa: E501
            return data

    def create_campaign_with_http_info(self, **kwargs):  # noqa: E501
        """Create New Campaign  # noqa: E501

        Creates a new campaign. The created campaign is a draft and is not automatically sent.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_campaign_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str list_id:
        :param str template_id:
        :param str from_email:
        :param str from_name:
        :param str subject:
        :param str name:
        :param bool use_smart_sending:
        :param bool add_google_analytics:
        :return: Campaign
                 If the method is called asynchronously,
                 returns the request thread.
        """


        all_params = ['list_id', 'template_id', 'from_email', 'from_name', 'subject', 'name', 'use_smart_sending', 'add_google_analytics']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_campaign" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}


        form_params = []
        local_var_files = {}
        if 'list_id' in params:
            form_params.append(('list_id', params['list_id']))  # noqa: E501
        if 'template_id' in params:
            form_params.append(('template_id', params['template_id']))  # noqa: E501
        if 'from_email' in params:
            form_params.append(('from_email', params['from_email']))  # noqa: E501
        if 'from_name' in params:
            form_params.append(('from_name', params['from_name']))  # noqa: E501
        if 'subject' in params:
            form_params.append(('subject', params['subject']))  # noqa: E501
        if 'name' in params:
            form_params.append(('name', params['name']))  # noqa: E501
        if 'use_smart_sending' in params:
            form_params.append(('use_smart_sending', params['use_smart_sending']))  # noqa: E501
        if 'add_google_analytics' in params:
            form_params.append(('add_google_analytics', params['add_google_analytics']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKeyAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v1/campaigns', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Campaign',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_campaign_info(self, campaign_id, **kwargs):  # noqa: E501
        """Get Campaign Info  # noqa: E501

        Returns summary information for the campaign specified.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_campaign_info(campaign_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str campaign_id: (required)
        :return: Campaign
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_campaign_info_with_http_info(campaign_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_campaign_info_with_http_info(campaign_id, **kwargs)  # noqa: E501
            return data

    def get_campaign_info_with_http_info(self, campaign_id, **kwargs):  # noqa: E501
        """Get Campaign Info  # noqa: E501

        Returns summary information for the campaign specified.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_campaign_info_with_http_info(campaign_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str campaign_id: (required)
        :return: Campaign
                 If the method is called asynchronously,
                 returns the request thread.
        """


        all_params = ['campaign_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_campaign_info" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'campaign_id' is set
        if ('campaign_id' not in params or
                params['campaign_id'] is None):
            raise ValueError("Missing the required parameter `campaign_id` when calling `get_campaign_info`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'campaign_id' in params:
            path_params['campaign_id'] = params['campaign_id']  # noqa: E501

        query_params = []

        header_params = {}


        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKeyAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v1/campaign/{campaign_id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Campaign',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_campaign_recipients(self, campaign_id, **kwargs):  # noqa: E501
        """Get Campaign Recipients  # noqa: E501

        Returns summary information about email recipients for the campaign specified that includes each recipients email, customer ID, and status.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_campaign_recipients(campaign_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str campaign_id: (required)
        :param int count: For pagination, the number of results to return. Max = 25,000
        :param str sort: Sort order to apply to results, either ascending or descending. Valid values are `asc` or `desc`. Defaults to `asc`.
        :param str offset: For pagination, if a response to this endpoint includes a `next_offset`, use that value to get the next page of recipients.
        :return: InlineResponse20012
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_campaign_recipients_with_http_info(campaign_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_campaign_recipients_with_http_info(campaign_id, **kwargs)  # noqa: E501
            return data

    def get_campaign_recipients_with_http_info(self, campaign_id, **kwargs):  # noqa: E501
        """Get Campaign Recipients  # noqa: E501

        Returns summary information about email recipients for the campaign specified that includes each recipients email, customer ID, and status.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_campaign_recipients_with_http_info(campaign_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str campaign_id: (required)
        :param int count: For pagination, the number of results to return. Max = 25,000
        :param str sort: Sort order to apply to results, either ascending or descending. Valid values are `asc` or `desc`. Defaults to `asc`.
        :param str offset: For pagination, if a response to this endpoint includes a `next_offset`, use that value to get the next page of recipients.
        :return: InlineResponse20012
                 If the method is called asynchronously,
                 returns the request thread.
        """


        all_params = ['campaign_id', 'count', 'sort', 'offset']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_campaign_recipients" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'campaign_id' is set
        if ('campaign_id' not in params or
                params['campaign_id'] is None):
            raise ValueError("Missing the required parameter `campaign_id` when calling `get_campaign_recipients`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'campaign_id' in params:
            path_params['campaign_id'] = params['campaign_id']  # noqa: E501

        query_params = []
        if 'count' in params:
            query_params.append(('count', params['count']))  # noqa: E501
        if 'sort' in params:
            query_params.append(('sort', params['sort']))  # noqa: E501
        if 'offset' in params:
            query_params.append(('offset', params['offset']))  # noqa: E501

        header_params = {}


        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKeyAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v1/campaign/{campaign_id}/recipients', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20012',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_campaigns(self, **kwargs):  # noqa: E501
        """Get Campaigns  # noqa: E501

        Returns a list of all the campaigns you've created. The campaigns are returned in reverse sorted order by the time they were created.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_campaigns(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page: For pagination, which page of results to return. Default = 0
        :param int count: For pagination, the number of results to return. Max = 100
        :return: InlineResponse20010
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_campaigns_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_campaigns_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_campaigns_with_http_info(self, **kwargs):  # noqa: E501
        """Get Campaigns  # noqa: E501

        Returns a list of all the campaigns you've created. The campaigns are returned in reverse sorted order by the time they were created.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_campaigns_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page: For pagination, which page of results to return. Default = 0
        :param int count: For pagination, the number of results to return. Max = 100
        :return: InlineResponse20010
                 If the method is called asynchronously,
                 returns the request thread.
        """


        all_params = ['page', 'count']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_campaigns" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'count' in params:
            query_params.append(('count', params['count']))  # noqa: E501

        header_params = {}


        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKeyAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v1/campaigns', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20010',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def schedule_campaign(self, campaign_id, **kwargs):  # noqa: E501
        """Schedule a Campaign  # noqa: E501

        Schedules a campaign for a time in the future  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.schedule_campaign(campaign_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str campaign_id: (required)
        :param str send_time:
        :return: InlineResponse20011
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.schedule_campaign_with_http_info(campaign_id, **kwargs)  # noqa: E501
        else:
            (data) = self.schedule_campaign_with_http_info(campaign_id, **kwargs)  # noqa: E501
            return data

    def schedule_campaign_with_http_info(self, campaign_id, **kwargs):  # noqa: E501
        """Schedule a Campaign  # noqa: E501

        Schedules a campaign for a time in the future  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.schedule_campaign_with_http_info(campaign_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str campaign_id: (required)
        :param str send_time:
        :return: InlineResponse20011
                 If the method is called asynchronously,
                 returns the request thread.
        """


        all_params = ['campaign_id', 'send_time']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method schedule_campaign" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'campaign_id' is set
        if ('campaign_id' not in params or
                params['campaign_id'] is None):
            raise ValueError("Missing the required parameter `campaign_id` when calling `schedule_campaign`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'campaign_id' in params:
            path_params['campaign_id'] = params['campaign_id']  # noqa: E501

        query_params = []

        header_params = {}


        form_params = []
        local_var_files = {}
        if 'send_time' in params:
            form_params.append(('send_time', params['send_time']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKeyAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v1/campaign/{campaign_id}/schedule', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20011',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def send_campaign(self, campaign_id, **kwargs):  # noqa: E501
        """Send a Campaign Immediately  # noqa: E501

        Queues a campaign for immediate delivery  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.send_campaign(campaign_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str campaign_id: (required)
        :return: InlineResponse20011
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.send_campaign_with_http_info(campaign_id, **kwargs)  # noqa: E501
        else:
            (data) = self.send_campaign_with_http_info(campaign_id, **kwargs)  # noqa: E501
            return data

    def send_campaign_with_http_info(self, campaign_id, **kwargs):  # noqa: E501
        """Send a Campaign Immediately  # noqa: E501

        Queues a campaign for immediate delivery  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.send_campaign_with_http_info(campaign_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str campaign_id: (required)
        :return: InlineResponse20011
                 If the method is called asynchronously,
                 returns the request thread.
        """


        all_params = ['campaign_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method send_campaign" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'campaign_id' is set
        if ('campaign_id' not in params or
                params['campaign_id'] is None):
            raise ValueError("Missing the required parameter `campaign_id` when calling `send_campaign`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'campaign_id' in params:
            path_params['campaign_id'] = params['campaign_id']  # noqa: E501

        query_params = []

        header_params = {}


        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKeyAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v1/campaign/{campaign_id}/send', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20011',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_campaign(self, campaign_id, **kwargs):  # noqa: E501
        """Update Campaign  # noqa: E501

        Updates details of a campaign. You can update a campaign's name, subject, from email address, from name, template or list.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_campaign(campaign_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str campaign_id: (required)
        :param str list_id:
        :param str template_id:
        :param str from_email:
        :param str from_name:
        :param str subject:
        :param str name:
        :param bool use_smart_sending:
        :param bool add_google_analytics:
        :return: Campaign
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_campaign_with_http_info(campaign_id, **kwargs)  # noqa: E501
        else:
            (data) = self.update_campaign_with_http_info(campaign_id, **kwargs)  # noqa: E501
            return data

    def update_campaign_with_http_info(self, campaign_id, **kwargs):  # noqa: E501
        """Update Campaign  # noqa: E501

        Updates details of a campaign. You can update a campaign's name, subject, from email address, from name, template or list.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_campaign_with_http_info(campaign_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str campaign_id: (required)
        :param str list_id:
        :param str template_id:
        :param str from_email:
        :param str from_name:
        :param str subject:
        :param str name:
        :param bool use_smart_sending:
        :param bool add_google_analytics:
        :return: Campaign
                 If the method is called asynchronously,
                 returns the request thread.
        """


        all_params = ['campaign_id', 'list_id', 'template_id', 'from_email', 'from_name', 'subject', 'name', 'use_smart_sending', 'add_google_analytics']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_campaign" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'campaign_id' is set
        if ('campaign_id' not in params or
                params['campaign_id'] is None):
            raise ValueError("Missing the required parameter `campaign_id` when calling `update_campaign`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'campaign_id' in params:
            path_params['campaign_id'] = params['campaign_id']  # noqa: E501

        query_params = []

        header_params = {}


        form_params = []
        local_var_files = {}
        if 'list_id' in params:
            form_params.append(('list_id', params['list_id']))  # noqa: E501
        if 'template_id' in params:
            form_params.append(('template_id', params['template_id']))  # noqa: E501
        if 'from_email' in params:
            form_params.append(('from_email', params['from_email']))  # noqa: E501
        if 'from_name' in params:
            form_params.append(('from_name', params['from_name']))  # noqa: E501
        if 'subject' in params:
            form_params.append(('subject', params['subject']))  # noqa: E501
        if 'name' in params:
            form_params.append(('name', params['name']))  # noqa: E501
        if 'use_smart_sending' in params:
            form_params.append(('use_smart_sending', params['use_smart_sending']))  # noqa: E501
        if 'add_google_analytics' in params:
            form_params.append(('add_google_analytics', params['add_google_analytics']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKeyAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v1/campaign/{campaign_id}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Campaign',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
