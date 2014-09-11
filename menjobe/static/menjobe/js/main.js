$(document).ready(function()
{
	$('.carousel').carousel({
		interval: 5000
		});
	$("[data-toggle=tooltip]").tooltip();

	//Handles menu drop down`enter code here`
	$('.dropdown-menu').find('form').click(function (e) {
		e.stopPropagation();
	});

});

$(function () {
	msg_loadingData = "S'esta carregant la informació...";
	msg_noRetailerProducts = "No hi ha productes per aquest punt de venda";
	msg_noProductRetailers = "No hi ha punts de venda pel producte";
	msg_loadError = "S'ha produït un error quan es carregava la informació";
	msg_noDescription = "No hi ha descripció";

	function productSelectFormat(product) {
		if (!product.id) return product.name; // optgroup
		return "<img class='menuicon' src='"
			+ staticFile('menjobe/images/product.png')+"'/> " + product.name;
	}

	function setupProductSelector(values) {
		products = values;
		for (var i=0; i<values.length; i++)
			values[i].text = values[i].name;
		$("#productselector").select2({
			allowClear: true,
			data: products,
			formatResult: productSelectFormat,
			formatSelection: productSelectFormat,
			dropdownCssClass: "bigdrop",
//			escapeMarkup: function (m) { return m; } // as is
			}).change(function(val) {
				if (!val.added) return;
				queryProductRetailers(val.added.id, val.added.name);
			});
		}

	function queryProductRetailers(productId, productName) {
		$('#producttitle').html(productName)
		$('#retailersList').html('<a class="list-group-item">Cercant...</a>');
		$.ajax({
			type: 'GET',
			datatype: 'json',
			url: '/json/productretailers/'+productId,
			success: function(data) {
				loadProductRetailers(data);
			},
		});
		$('#addProductRetailerBtn').attr('href', "/admin/menjobe/retailpoint/");
	}

	function loadProductRetailers(retailers) {
		$('#page-retailerInfo').addClass('hidden');
		$('#page-retailerProducts').addClass('hidden');
		html=[]
		if (retailers.length==0)
			html.push(
				"<a class='list-group-item list-group-item-danger'>"
				+msg_noProductRetailers+'</a>');
		$.each(retailers, function(i, row) {
			html.push(
				$('<a>').attr({
					'class': 'list-group-item list-item-product-retailer',
					'data-id': row.id,
					}).text(row.name)
				);
			});
		$('#retailersList').html(html);
		$('.list-item-product-retailer').click(function () {
			$('#retailersList .list-group-item').removeClass('active');
			$(this).addClass("active");
			loadProductDetails($(this));
		});
	}
	$('#retailerinfo_productsbtn').click(function() {
		var page = $('#page-retailerInfo')
		var retailerId = page.attr("data-id");
		var retailerName = page.attr("data-name");
		queryRetailerProducts(retailerId, retailerName)
	});

	function loadProductDetails(link) {
		var retailerId = $(link).attr('data-id');
		var retailerName = $(link).html();
		var descriptionTag = $('#retailerinfo_description');
		$("#page-retailerInfo").attr('data-id', retailerId);
		$("#page-retailerInfo").attr('data-name', retailerName);
		descriptionTag.removeClass();
		descriptionTag.addClass("alert alert-info");
		descriptionTag.html(msg_loadingData);
		$('#retailerinfo_name').html(retailerName);
		$('#retailerinfo_address').html("");
		$('#page-retailerInfo').removeClass('hidden');
		$.ajax({
			type: 'GET',
			datatype: 'json',
			url: '/json/retailer/'+retailerId,
			error: function(response) {
				descriptionTag.removeClass();
				descriptionTag.addClass("alert alert-error");
				descriptionTag.html(msg_loadError);
			},
			success: function(data) {
				descriptionTag.removeClass();
				descriptionTag.html(data.descriptionHtml || "<p class='panel-warning'>"+msg_noDescription+"</p>" );
				$('#retailerinfo_address').html(data.address);
				$('#retailerinfo_editbtn').attr('href', "/admin/menjobe/retailpoint/"+retailerId);
			},
		});
		queryRetailerProducts(retailerId, retailerName);
	}

	function queryRetailerProducts(retailerId, retailerName) {
		$('#page-retailerProducts').removeClass('hidden');
		$('#page-retailerProducts #retailertitle').html(retailerName)
		$('#page-retailerProducts #productList').html($('<a>').attr({
			class: 'list-group-item list-group-item-info'
			}).text(msg_loadingData));
		$.ajax({
			type: 'GET',
			datatype: 'json',
			url: '/json/retailer/'+retailerId+'/products',
			error: function(response) {
				alert("TODO: No he pogut baixar els productes del canal");
			},
			success: function(products) {
				renderRetailerProducts(products);
			},
		});
	}

	function renderRetailerProducts(products) {
		$('#page-*').addClass('hidden');
		$('#page-retailerProducts').removeClass('hidden');
		html=[]
		if (products.length==0)
			html.push(
				"<a class='list-group-item list-group-item-danger'>"
				+msg_noRetailerProducts+'</a>');
		$.each(products, function(i, row) {
			html.push(
				$('<a>').attr({
					'class': 'list-group-item list-item-retailer-product',
					'data-id': row.id,
					}).text(row.name)
				);
			});
		$('#productList').html(html);
	}

	function hideAllPages() {
		pages = $("[id^='page-']");
		pages.addClass('hidden');
	}

	function navChange(tabid) {
		
		$('#menjobe_menubar .active').removeClass('active')
		$(tabid).addClass('active');
		hideAllPages();
	}

	function channelSearch() {
		notImplemented();
		return;
		navChange('#navbar-channelsTab');
		$('#page-notimplemented').removeClass('hidden');
	}

	function producerSearch() {
		notImplemented();
		return;
		navChange('#navbar-producersTab');
		$('#page-notimplemented').removeClass('hidden');
	}

	function productSearch()
	{
		navChange('#navbar-productsTab');
		$('#page-productSearch').removeClass('hidden');
		$('#page-productRetailers').removeClass('hidden');
		$.ajax({
			type: 'GET',
			datatype: 'json',
			url: '/json/allproducts',
			success: function(data) {
				setupProductSelector(data);
			},
		});
	}

	function showFrontPage() {
		navChange('#navbar-none');
		$('#page-frontpage').removeClass('hidden');a
	}
	
	$('.navbar-brand').click(showFrontPage);
	$('#navbar-productsTab').click(productSearch);
	$('#navbar-channelsTab').click(channelSearch);
	$('#navbar-producersTab').click(producerSearch);

	$('#btn-productsTab').click(productSearch);
	$('#btn-channelsTab').click(channelSearch);
	$('#btn-producersTab').click(producerSearch);
});

function notImplemented() {
	$('#notImplemented').modal('show');
}


function debug(obj) {
	result = "";
	$.each(obj, function (key,val) {
		result += key+": "+val+'\n';
	});
	return result;
}

