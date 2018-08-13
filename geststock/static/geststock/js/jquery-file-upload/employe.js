$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-employe .modal-content").html("");
        $("#modal-employe").modal("show");
      },
      success: function (data) {
        $("#modal-employe .modal-content").html(data.html_form);
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
          $("#employe-table tbody").html(data.html_employe_list);
          $("#modal-employe").modal("hide");
        }
        else {
          $("#modal-employe .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create employe
  $(".js-create-employe").click(loadForm);
  $("#modal-employe").on("submit", ".js-employe-create-form", saveForm);

  // Update employe
  $("#employe-table").on("click", ".js-update-employe", loadForm);
  $("#modal-employe").on("submit", ".js-employe-update-form", saveForm);

  // Delete employe
  $("#employe-table").on("click", ".js-delete-employe", loadForm);
  $("#modal-employe").on("submit", ".js-employe-delete-form", saveForm);

});
