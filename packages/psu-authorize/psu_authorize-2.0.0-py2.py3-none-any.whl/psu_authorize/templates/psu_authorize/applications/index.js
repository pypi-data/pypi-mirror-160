{% load base_taglib %}

$(document).ready(function() {
    var application_table = $('#applications_table').DataTable( {
        "pageLength": 50,
        "pagingType": "full_numbers"
    } );
    //Focus on the search box on page load
    $('#application_table_filter').find('input[type=search]').focus();
} );

function new_application(){
    var app_form = $('#application-form');
    var app_code = app_form.find('#app_code').val();
    var app_title = app_form.find('#app_title').val();
    var application_button = app_form.find('#new-application-btn');
    $.ajax({
        type:   "POST",
        url:    "{%url 'authorize:new_applications'%}",
        data:   {
            app_title: app_title, app_code: app_code,
            csrfmiddlewaretoken: '{{csrf_token}}'
        },
         beforeSend:function(){
            application_button.after(getAjaxLoadImage());},
        success:function(data){
            console.log('Successful');
            console.log(data);
            var table = $('#applications_table');
            table.find('tr:first').after(data);
            new_row = table.find('tr').eq(1);
            table.DataTable().row.add(new_row).draw();
            },
        error:function(){
            console.log("failed");},
        complete:function(){
            clearAjaxLoadImage(application_button.parent());
        }
    });
}
