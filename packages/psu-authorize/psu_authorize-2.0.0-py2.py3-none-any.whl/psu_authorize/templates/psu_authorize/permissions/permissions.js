$(document).ready(function() {
    var permission_table = $('#permission_table').DataTable( {
        "pageLength": 50,
        "pagingType": "full_numbers"
    } );
    var global_table = $('#global_table').DataTable( {
        "pageLength": 50,
        "pagingType": "full_numbers"
    } );

    //Search Boxes on local and global tables
    var local_search_input = $('#permission_table_filter').find('input[type=search]');
    var global_search_input = $('#global_table_filter').find('input[type=search]');
    //Sync the two search boxes
    local_search_input.keyup(function(){
        global_table.search(local_search_input.val()).draw();;
    });
    global_search_input.keyup(function(){
        permission_table.search(global_search_input.val()).draw();;
    });
    //Hide the global search to avoid confusion
    $('#global_table_filter').addClass('hidden');
    //Focus on the search box on page load
    local_search_input.focus();
});

function toggle_grant_form(){
    var btn = $('#grant-permission-btn');
    var form = $('#grant-permission-form');
    if(form.hasClass('hidden')){
        form.removeClass('hidden');
        btn.addClass('hidden');
    }
    else{
        form.addClass('hidden');
        btn.removeClass('hidden');
    }
}

function grant_permission(){
    var grant_form = $('#grant-permission-form');
    var app_code = grant_form.find('#grant_application').val();
    var authority_id = grant_form.find('#grant_authority').val();
    var grantee = grant_form.find('#grant_grantee').val();
    var grant_button = grant_form.find('#grant-permission-btn');

    $.ajax({
            type:   "POST",
            url:    "{%url 'authorize:grant_permission'%}",
            data:   {
                app_code: app_code, authority_id: authority_id, grantee: grantee,
                csrfmiddlewaretoken: '{{csrf_token}}'
            },
            beforeSend:function(){
                grant_button.after(getAjaxLoadImage());
                grant_button.addClass('hidden');
            },
            success:function(data){
                console.log('Successful grant');
                console.log(data);
                var table = $('#permission_table');
                table.find('tr:first').after(data);
                new_row = table.find('tr').eq(1);
                table.DataTable().row.add(new_row).draw();
            },
            error:function(){
            },
            complete:function(){
                grant_button.removeClass('hidden');
                clearAjaxLoadImage(grant_button.parent());
            }
        });
}

function revoke_permission(id){
    try{
        var table = $('#permission_table').DataTable();
        var rows = $('.row-'+id);
        var num_users = rows.length;
        var authority = rows.first().find('.pp-auth').html();
        if(num_users > 1){
            var assignee = rows.first().find('.pp-via').html();
        }
        else{
            var assignee = rows.first().find('.pp-user').html();
        }

        var msg = 'Revoke '+authority+' from '+assignee+'?';
        if(num_users > 1){
            msg += ' This will affect '+num_users+' users.';
        }
        if(confirm(msg)){
            console.log(msg);
            $.ajax({
                type:   "POST",
                url:    "{%url 'authorize:revoke_permission_tbd'%}/"+id+"/",
                data:   { csrfmiddlewaretoken: '{{csrf_token}}' },
                beforeSend:function(){
                    rows.find('.pp-act').append(getAjaxLoadImage());
                },
                success:function(data){
                    console.log('Success');
                    rows.each(function(){
                        var thisRow = $(this);
                        table.row(thisRow).remove();
                    });
                    rows.remove();
                    table.draw();
                },
                error:function(){
                    clearAjaxLoadImage();
                    rows.find('.pp-act').html(getAjaxSaveFailedIcon("Revoke failed"));
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