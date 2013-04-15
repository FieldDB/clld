<table id="${datatable.eid}" cellpadding="0" cellspacing="0" border="0" class="table table-condensed table-bordered table-striped">
    <thead>
        <tr>
            % for col in datatable.cols:
            <th>${col.js_args['sTitle']}</th>
            % endfor
        </tr>
    </thead>
    <tbody>
    </tbody>
    <tfoot>
	<tr>
            % for col in datatable.cols:
	    <th style="text-align: left;">
                % if col.js_args.get('bSearchable', True):
		    % if hasattr(col, 'choices'):
		    <select class="control" name="${col.name}">
			<option value="">--any--</option>
			% for val in getattr(col, 'choices'):
			    % if isinstance(val, tuple) and len(val) == 2:
			    <option value="${val[0]}">${val[1]}</option>
			    % else:
			    <option value="${val}">${val}</option>
			    % endif
			% endfor
		    </select>
		    % else:
		    <input type="text" name="${col.name}" value="" placeholder="Search ${col.js_args['sTitle']}" class="input-small control" />
		    % endif
                % else:
                    <input type="text" name="${col.name}" value="" class="search_init control" style="display: none;"/>
                % endif
            </th>
            % endfor
	</tr>
    </tfoot>
</table>
<script>
$(document).ready(function() {
    ${h.JSDataTable.init(datatable.eid, datatable.toolbar(), datatable.options)|n};
});
</script>
