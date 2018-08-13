$function() {
	/* Ouvrir l'explorateur */
	$(".js-upload-photos").click(function(){
		$("#fileupload").click();
	});

	/* On initialise les fichiers à uploader */
	$("#fileupload").fileupload({
		datatType: 'json',
		sequentialsUploads: true, /* Envoyer les fichiers un par un */
		start: function(e) { /* Quand l'upload commence, lancer la barre de progression */ 
			$("#modal-progress").modal("show");
		},
		stop: function(e) { /* Quand l'upload finit, fermer la barre de progression */ 
			$("#modal-progress").modal("hide");
		},
		progressall: function(e, data) { /* mettre à jour la barre de progression */ 
			var progress = parseInt(data.loaded / data.total * 100, 10);
			var strProgress = progress + "%";
			$("#.progress-bar").css({"width": strProgress});
			$("#.progress-bar").text(strProgress);
		},
		done: function (e, data) {
			/* Preparons la reponse du serveur */
			if (data.result.is_valid) {
				$("#gallery tbody").prepend(
					"<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
				)
			}
		}
	});
}