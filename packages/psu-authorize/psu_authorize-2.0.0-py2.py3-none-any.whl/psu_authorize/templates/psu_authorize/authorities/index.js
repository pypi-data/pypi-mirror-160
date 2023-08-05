{% load base_taglib %}

$(document).ready(function() {
    var authority_table = $('#authority_table').DataTable( {
        "pageLength": 50,
        "pagingType": "full_numbers"
    } );
    //Focus on the search box on page load
    $('#authority_table_filter').find('input[type=search]').focus();
} );


function new_authority(){
    var auth_form = $('#authority-form');
    var authority_code = auth_form.find('#auth_code').val();
    var title = auth_form.find('#auth_title').val();
    var description = auth_form.find('#auth_desc').val();
    var authority_button = auth_form.find('#new-authority-btn');
    $.ajax({
            type:   "POST",
            url:    "{%url 'authorize:new_authorities'%}",
            data:   {
                title: title, authority_code: authority_code, description: description,
                csrfmiddlewaretoken: '{{csrf_token}}'
            },
             beforeSend:function(){
                authority_button.after(getAjaxLoadImage());},
            success:function(data){
                console.log('Successfully created an authority');
                console.log(data);
                console.log(description);
                var table = $('#authority_table');
                table.find('tr:first').after(data);
                new_row = table.find('tr').eq(1);
                table.DataTable().row.add(new_row).draw();
            },
            error:function(){
                console.log("failed to create an authority");},
            complete:function(){
                clearAjaxLoadImage(authority_button.parent());
            }
            });
    }

{% if global_access%}
function delete_authority(id){
    try{
        var table = $('#authority_table').DataTable();
        var rows = $('.row-'+id);
        var code = rows.first().find('.auth-code').html();
        var msg = 'Deleting will revoke all the assigned permissions to the '+code+' authority. Are you sure you want to delete?';

        if(confirm(msg)){
            console.log(msg);
            $.ajax({
                type:   "POST",
                url:    "{%url 'authorize:delete_authority'%}/"+id+"/",
                data:   { csrfmiddlewaretoken: '{{csrf_token}}'},
                beforeSend:function(){
                    rows.find('.auth-act').append(getAjaxLoadImage());
                },
                success:function(data){
                    console.log('data');
                    rows.each(function(){
                        var thisRow = $(this);
                        table.row(thisRow).remove();
                        });
                    rows.remove();
                    table.draw();
                },
                error:function(){
                    clearAjaxLoadImage();
                    rows.find('.pp-act').html(getAjaxSaveFailedIcon("Deleting an authority failed"));
                },
                complete:function(){
                }
            });
        }
    }
    catch(ee){
        alert(ee);
    }
 }
 {%endif%}