
var allMetadata = null;
var currPgnMetadata = null;
var currPgnData = null;

$(document).ready(function() {

	$.getJSON(url="pgn_index.json", success=function(jsonData, textStatus, jqXHR) {
		allMetadata = jsonData;

		$("#pgnFileChooser").html("");
		for (var i = 0; i < allMetadata.length; i++) {
			var pgnMetadata = allMetadata[i];
			$("#pgnFileChooser").append("<li><a href=\"#\">" + pgnMetadata.label + "</a></li>");
		}

		$("#pgnFileChooser a").click(function(e) {
			e.preventDefault();

			//load chosen pgn
			currPgnMetadata = allMetadata[$(this).parent().index()];
			var gamesMetadata = currPgnMetadata.games;
			var pgnPath = currPgnMetadata.file;
			$.get(url=pgnPath, success=function(pgnData) {
				currPgnData = pgnData;
				//update games table
				$("#gamesTable tbody").html("");
				for (var i = 0; i < gamesMetadata.length; i++) {
					var g = gamesMetadata[i];
					$("#gamesTable tbody").append("<tr>" 
						+ "<td>" + g.Date + "</td>"
						+ "<td>" + g.Round + "</td>"
						+ "<td>" + g.White + "</td>"
						+ "<td>" + g.WhiteElo + "</td>"
						+ "<td>" + g.BlackElo + "</td>"
						+ "<td>" + g.Black + "</td>"
						+ "<td>" + g.Result + "</td>"
						+ "</tr>");
				}

				$("#gamesTable tbody tr").click(function(e) {
					e.preventDefault();
					$(this).addClass('highlight').siblings().removeClass('highlight');

					//update game metadata panel
					var g = currPgnMetadata.games[$(this).index()];
					$("#gameMetadata .players").text(g.White + "(" + g.WhiteElo + ") - " + g.Black + "(" + g.BlackElo + ")");
					$("#gameMetadata .result").text(g.Result);
					$("#gameMetadata .opening").text(g.ECO);
					$("#gameMetadata .site_and_date").text(g.Event 
						+ (g.Site != null &&  g.Site != "" ? ", " + g.Site : "")
						+ ", " + g.Date);

					//update chessboard
					var pgnStr = g.movetext;
					$("#myboard-container").html("");
					$("#myboard-moves").html("");
					var ctPgnViewer = new PgnViewer({
						boardName: "myboard",
						pgnString: pgnStr,
						pieceSet: 'merida',
						pieceSize: 46,
						movesFormat: 'default'
					});

				});
			});
		});
	});
});

/*
function getGamePgnString(iGame) {
	return currPgnData.movetext;
	alert(lines);

	var iGame = 0;
	parsing_state = PARSE_START;
	for (var i = 0; i < lines.length; i++) {
		var line = lines[i];
	}

	return "1. e4 b6 2. d4 e6 3. Bd3 Bb7";
} */