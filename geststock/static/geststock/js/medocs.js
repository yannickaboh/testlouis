$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-medoc .modal-content").html("");
        $("#modal-medoc").modal("show");
      },
      success: function (data) {
        $("#modal-medoc .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#medoc-table tbody").html(data.html_medoc_list);
          $("#modal-medoc").modal("hide");
        }
        else {
          $("#modal-medoc .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create medoc
  $(".js-create-medoc").click(loadForm);
  $("#modal-medoc").on("submit", ".js-medoc-create-form", saveForm);

  // Update medoc
  $("#medoc-table").on("click", ".js-update-medoc", loadForm);
  $("#modal-medoc").on("submit", ".js-medoc-update-form", saveForm);

  // Delete medoc
  $("#medoc-table").on("click", ".js-delete-medoc", loadForm);
  $("#modal-medoc").on("submit", ".js-medoc-delete-form", saveForm);

});
