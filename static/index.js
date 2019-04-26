function toggleUploadButton(uploading) {
  if (uploading) {
    $("#upload-text").text("UPLOADING");
    if ($("#upload-spinner").is(":hidden")) {
      $("#upload-spinner").show();
    }
  } else {
    $("#upload-text").text("UPLOAD");
    if ($("#upload-spinner").is(":visible")) {
      $("#upload-spinner").hide();
    }
  }
}

function uploadSuccess(response) {
  toggleUploadButton(false);
  $("#form-response").remove();
  $("#video-container").show();
  $("#video-preview").attr("src", response.path);
  $("#originalVideoTitle").html(response.title);
  $("#color-choose").show();
  $("html, body").animate({
    scrollTop: $("#video-container").offset().top
  });
  $("#video-submit").prop("disabled", "disabled");
}

function uploadError(message) {
  $("#upload-error").show();
  $("#upload-error").html(message);
  toggleUploadButton(false);
}

$(document).ready(function() {
  $(".navbar-brand").click(function() {
    if (window.location.pathname === '/') {
      $("html, body").animate({
        scrollTop: 0
      });
    } else {
      window.location.href = "/";
    }
  });

  $("#video-upload input").keyup(function() {
    $("#video-submit").prop("disabled", this.value == "" ? true : false);
  });

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
          uploadSuccess(response);
        },
        error: error => {
          let message;
          if (error.statusText === "timeout") {
            message = "Timeout! Request took too long";
          } else if (error.responseJSON) {
            message = error.responseJSON.message;
          } else {
            message = "Unknown error occured!";
          }
          uploadError(message);
        },
        timeout: 20000
      });
    } catch (e) {}
  });

  $(".picker").change(function() {
    console.log(this);
    let empty = true;
    $(".picker").each(function() {
      empty = this.value == "";
    });
    $("#color-submit").prop("disabled", empty);
  });

  $("#color-choose").on("submit", e => {
    e.preventDefault();
  });

  $(".picker").loads({
    layout: "rgb",
    flat: false,
    enableAlpha: false,
    onChange: function(ev) {
      $(ev.el).css("border-color", "#" + ev.hex);
      $(ev.el).val("#" + ev.hex).trigger('change');
      $(ev.el).setColor("#" + ev.hex, false);
    },
    onSubmit: function(ev) {
      $(ev.el).hides();
    },
  });
});
