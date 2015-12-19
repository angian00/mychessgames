
var allMetadata = null;

$(document).ready(function() {

	$.get({url: "pgn_index.json", success: function(jsonData) {
			allMetadata = jsonData;

			for (pgnData in allMetadata) {
				$("#pgnFileChooser").append("<li><a href=\"#\">" + pgnData.label + "</a></li>");
			}

			$("#pgnFileChooser a").click(function(e) {
				e.preventDefault();
				alert("You have chosen file #" + $(this).parent().index());
			});
		}
	});
});
