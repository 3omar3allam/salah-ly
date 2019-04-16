$(function() {
  $('#video-upload').on('submit', e => {
    $('#form-response').html('Please wait...');
    e.preventDefault();
    var form = $('#video-upload').serialize();
    $.ajax({
      url: '/',
      method: 'post',
      data: form,
      processData: false,
      success: response => {
        $('#form-response').remove();
        $('#video-preview').attr('src',response.path);
        $('#video-preview').removeAttr('hidden')

      }
    });
  });
});
