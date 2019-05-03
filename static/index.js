(color1 = {
  h: 0,
  s: 100,
  b: 100
}),
  (color2 = {
    h: 240,
    s: 100,
    b: 100
  });

function toggleUploadButton(uploading) {
  if (uploading) {
    $("#upload-text").text("FETCHING");
    if ($("#upload-spinner").is(":hidden")) {
      $("#upload-spinner").show();
    }
  } else {
    $("#upload-text").text("FETCH");
    if ($("#upload-spinner").is(":visible")) {
      $("#upload-spinner").hide();
    }
  }
}

function uploadSuccess(response) {
  sessionStorage.setItem('videoTitle', response.title);
  sessionStorage.setItem('videoPath', response.path);
  resetColors();
  $("#result-download").hide();
  toggleUploadButton(false);
  $("#form-response").remove();
  $("#video1-container").show();
  $("#video1-preview").attr("src", response.path);
  $("#originalVideoTitle").html(response.title);
  $("#color-choose").show();
  $("html, body").animate({
    scrollTop: $("#video1-container").offset().top - 60
  });
}

function uploadError(message) {
  $("#upload-error").show();
  $("#upload-error").html(message);
  toggleUploadButton(false);
}

function toggleConvertButton(converting) {
  if (converting) {
    $("#color-text").text("CONVERTING");
    if ($("#color-spinner").is(":hidden")) {
      $("#color-spinner").show();
    }
  } else {
    $("#color-text").text("CONVERT");
    if ($("#color-spinner").is(":visible")) {
      $("#color-spinner").hide();
    }
  }
}

function convertSuccess(response) {
  resetColors();
  toggleConvertButton(false);
  $("#result-download").show();
  $("#result-download").attr("href", response.path);
  // $("#video2-container").show();
  // $("#video2-preview").attr("src", response.path);
  // $("html, body").animate({
  //   scrollTop: $("#video2-container").offset().top - 60
  // });
}

function convertError(message) {
  resetColors();
  $("#convert-error").show();
  $("#convert-error").html(message);
  toggleConvertButton(false);
  $("#result-download").hide();
}

function resetColors() {
  (color1 = {
    h: 0,
    s: 100,
    b: 100
  }),
    (color2 = {
      h: 240,
      s: 100,
      b: 100
    });
}

$(document).ready(function() {
  resetColors();
  $(".navbar-brand").click(function() {
    if (window.location.pathname === "/") {
      $("html, body").animate({
        scrollTop: 0
      });
    } else {
      window.location.href = "/";
    }
  });
  $("#video-upload input").on("input", function() {
    $("#video-submit").prop("disabled", this.value == "" ? true : false);
  });

  $("#video-upload").on("submit", e => {
    e.preventDefault();
    toggleUploadButton(true);
    if ($("#upload-error").is(":visible")) {
      $("#upload-error").hide();
    }
    if ($("#video1-container").is(":visible")) {
      $("#video1-preview").removeAttr("src");
      $("#video1-container").hide();
    }
    var formData = $("#video-upload").serialize();
    const url = $("#video-upload input[name=url]").val();
    if (url === sessionStorage.getItem("videoUrl") && sessionStorage.getItem('videoPath')) {
      const fakeResponse = {
        path: sessionStorage.getItem('videoPath'),
        title: sessionStorage.getItem("videoTitle")
      };
      uploadSuccess(fakeResponse);
    } else {
      try {
        $.ajax({
          url: "/",
          method: "post",
          data: formData,
          processData: false,
          success: response => {
            sessionStorage.setItem('videoUrl', url);
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
          timeout: 300000000
        });
      } catch (e) {
        uploadError(e.message);
      }
    }
  });

  $(".picker").loads({
    layout: "rgb",
    flat: false,
    enableAlpha: false,
    onChange: function(ev) {
      if (ev.el.id === "picker1") {
        color1 = ev.hsb;
      } else if (ev.el.id === "picker2") {
        color2 = ev.hsb;
      }
      $(ev.el).css("border-color", "#" + ev.hex);
      $(ev.el)
        .val("#" + ev.hex)
        .trigger("change");
      $(ev.el).setColor("#" + ev.hex, false);
    },
    onSubmit: function(ev) {
      $(ev.el).hides();
    }
  });

  $("#color-form").on("submit", e => {
    e.preventDefault();
    toggleConvertButton(true);
    if ($("#convert-error").is(":visible")) {
      $("#convert-error").hide();
    }
    if ($("#video2-container").is(":visible")) {
      $("#video2-preview").removeAttr("src");
      $("#video2-container").hide();
    }
    try {
      var start = $("#color-form input[name=start]").val();
      var end = $("#color-form input[name=end]").val();
      if (!start) {
        start = 0;
      } else if (isNaN(parseInt(start))) {
        throw Error("Start must be a number!");
      }

      if (!end) {
        end = -1;
      } else if (isNaN(parseInt(end))) {
        throw Error("End must be a number!");
      }
      $.ajax({
        url: "/convert",
        method: "post",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: JSON.stringify({
          color1: color1,
          color2: color2,
          start: start,
          end: end
        }),
        success: response => {
          convertSuccess(response);
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
          convertError(message);
        }
      });
    } catch (e) {
      convertError(e.message);
    }
  });
});
