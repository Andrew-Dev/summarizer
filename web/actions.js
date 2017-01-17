function parseSummary(text) {
	var sentences = text.split("<<sentence>>");
	var summary = "";
	sentences.forEach(function(sentence) {
		summary += sentence + "<br><br>";
	});
	return summary;
}

function presentArticleSummary(text,title,img) {
	if(img != "") {
		$("#articleTitle").css("min-height", "320px");
		$("#articleTitle").css("background", "url('" + img + "') no-repeat center center fixed #46B6AC");
	}
	$("#articleTitle").html('<h2 class="mdl-card__title-text">' + title + '</h2>');
	$("#articleContent").html(text);
	$('body').css("overflow","scroll");
	$("#articleCard").fadeIn();
}

$(document).ready(function () {
	$("#articleCard").hide();
	$( "#summarizeBtn" ).click(function() {
		var url = $("#urlBox").val();
		if (!url.startsWith("http://"))
			url = "http://" + url;
  		var data = {length: $("#lengthBox").val(), url: url};
		$.ajax({
		    type: 'POST',
		    url: 'http://159.203.126.117:5000/articleSummarize/',
		    data: JSON.stringify(data),
		    success: function(data) 
		    { console.log(data);
			  var text = parseSummary(data["summary"]);
			  console.log(text)
			  presentArticleSummary(text,data["metadata"]["title"],data["metadata"]["img"])
		    },
		    contentType: "text/plain",
		});
	});
});