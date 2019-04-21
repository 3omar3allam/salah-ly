function toggleUploadButton(uploading) {
  if (uploading) {
    $("#upload-text").text("UPLOADING");
    $("#upload-spinner").removeAttr("hidden");
  } else {
    $("#upload-text").text("UPLOAD");
    if ($("#upload-spinner").is(":visible")) {
      $("#upload-spinner").hide();
    }
  }
}

function uploadError(response) {
  $("#upload-error").removeAttr("hidden");
  $("#upload-error").html(response.message);
  toggleUploadButton(false);
}

$(document).ready(function() {
  $("#video-upload").on("submit", e => {
    e.preventDefault();
    toggleUploadButton(true);
    if ($("#upload-error").is(":visible")) {
      $("#upload-error").hide();
    }
    if ($("#video-container").is(":visible")) {
      $("#video-preview").removeAttr("src");
      $("#video-container").hide();
    }
    var form = $("#video-upload").serialize();
    try {
      $.ajax({
        url: "/",
        method: "post",
        data: form,
        processData: false,
        success: response => {
          toggleUploadButton(false);
          $("#form-response").remove();
          $("#video-container").removeAttr("hidden");
          $("#video-preview").attr("src", response.path);
          $("#originalVideoTitle").html(response.title);
        },
        error: error => {
          uploadError(error.responseJSON);
        }
      });
    } catch (e) {}
  });

  $("#video-process").on("submit", e => {
    e.preventDefault();
  });
});
