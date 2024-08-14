var myDeviceID;
$(function(){ //DOM Ready

    function navigate(url)
    {
        window.location.href = url;
    }

    $(document).attr("title", "Main Panel");
    content_width = (120 + 5) * 8 + 5
    $('.gridster').width(content_width)
    $(".gridster ul").gridster({
        widget_margins: [5, 5],
        widget_base_dimensions: [120, 120],
        avoid_overlapped_widgets: true,
        max_rows: 15,
        max_size_x: 8,
        shift_widgets_up: false
    }).data('gridster').disable();

    // Add Widgets

    var gridster = $(".gridster ul").gridster().data('gridster');
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-baseclock-default-clock" id="default-clock"><h1 class="date"data-bind="text: date, attr: {style: date_style}"></h1><h2 class="time" data-bind="text: time, attr: {style: time_style}"></h2></div></li>', 2, 1, 1, 1)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-baseswitch-default-switch" id="default-switch"><span class="toggle-area" id="switch"></span><h1 class="title" data-bind="text: title, attr:{style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{style: title2_style}"></h1><h2 class="icon" data-bind="attr:{style: icon_style}"><i data-bind="attr: {class: icon}"></i></h2><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 2, 1, 1, 2)
    


    var widgets = {}
    // Initialize Widgets
    
        widgets["default-clock"] = new baseclock("default-clock", "", "default", {'widget_type': 'baseclock', 'fields': {'date': '', 'time': ''}, 'static_css': {'date_style': 'color: #fff;', 'time_style': 'color: #aa00ff;', 'widget_style': 'background-color: #444;'}, 'static_icons': [], 'icons': [], 'css': {}, 'use_comma': 0, 'precision': 1, 'use_hass_icon': 1, 'namespace': 'default'})
    
        widgets["default-switch"] = new baseswitch("default-switch", "", "default", {'widget_type': 'baseswitch', 'entity': 'switch.wemo_switch_1', 'state_active': 'on', 'state_inactive': 'off', 'enable': 1, 'post_service_active': {'service': 'homeassistant/turn_on', 'entity_id': 'switch.wemo_switch_1'}, 'post_service_inactive': {'service': 'homeassistant/turn_off', 'entity_id': 'switch.wemo_switch_1'}, 'fields': {'title': 'wemo_switch_1', 'title2': '', 'icon': '', 'icon_style': '', 'state_text': ''}, 'icons': {'icon_on': 'fas-circle', 'icon_off': 'far-circle'}, 'static_icons': [], 'css': {'icon_style_active': 'color: #aaff00;', 'icon_style_inactive': 'color: #888;'}, 'static_css': {'title_style': 'color: #fff;', 'title2_style': 'color: #fff;', 'state_text_style': 'color: #fff;', 'widget_style': 'background-color: #444;'}, 'use_comma': 0, 'precision': 1, 'use_hass_icon': 1, 'namespace': 'default'})
    

    // Setup click handler to cancel timeout navigations

    $( ".gridster" ).click(function(){
        clearTimeout(myTimeout);
        if (myTimeoutSticky) {
            myTimeout = setTimeout(function() { navigate(myTimeoutUrl); }, myTimeoutDelay);
        }
    });

    // Set up timeout

    var myTimeout;
    var myTimeoutUrl;
    var myTimeoutDelay;
    var myTimeoutSticky = 0;
    if (location.search != "")
    {
        console.log("begin")
        var query = location.search.substr(1);
        var result = {};
        query.split("&").forEach(function(part) {
        var item = part.split("=");
        result[item[0]] = decodeURIComponent(item[1]);
        });

        if ("deviceid" in result)
        {
            myDeviceID = result.deviceid;
            try
            {
                setCookie('ADdevID', myDeviceID);
            }
            catch (e)
            {
                console.log(e);
            }
        }
        else
        {
            try
            {
                myDeviceID = getCookie('ADdevID');
            }
            catch (e)
            {
                console.log(e);
                myDeviceID = null;
            }
        }
        if ("timeout" in result && "return" in result)
        {
            url = result.return
            argcount = 0
            for (arg in result)
            {
                if (arg != "timeout" && arg != "return" && arg != "sticky")
                {
                    if (argcount == 0)
                    {
                        url += "?";
                    }
                    else
                    {
                        url += "&";
                    }
                    argcount ++;
                    url += arg + "=" + result[arg]
                }
            }
            if ("sticky" in result)
            {
                myTimeoutSticky = (result.sticky == "1");
            }
            myTimeoutUrl = url;
            myTimeoutDelay = result.timeout * 1000;
            myTimeout = setTimeout(function() { navigate(url); }, result.timeout * 1000);
        }
    }
    else
    {
        try
        {
            myDeviceID = getCookie('ADdevID');
        }
        catch (e)
        {
            console.log(e);
            myDeviceID = null;
        }
    }

    // Start listening for AD Events

    window.dashstream = new DashStream("ws", location.protocol, document.domain, location.port, "Main Panel", widgets);

});