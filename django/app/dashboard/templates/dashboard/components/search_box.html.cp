<div class="card">
				<!--<a data-toggle="collapse" data-target="#search_body" aria-expanded="true" aria-controls="search_body" style=":hover {background-color: blue;}"><div class="card-header">
				Search Box
				</div></a>
				<div class="collapse" id="search_body">-->
				<div class="card-header">
								Search Box
				</div>
				<div>
								<div class="card-body">
												<div class="row mb-3">
																<div class="col-12">
																				<form action="" method="get">
																								<div class="input-group input-group-sm mb-3">
																												<input type="text" class="form-control" placeholder="Keyword1 Keyword2 ...(and search)" value="{% if query_params.keywords %}{{query_params.keywords}}{% endif %}" aria-label="Keyword" aria-describedby="basic-addon2" name="keywords">
																												<div class="input-group-append">
																																<button class="btn btn-secondary" type="submit">Search</button>
																												</div>
																								</div>

																								<div class="form-group row">
																												<label for="example-text-input" class="col-md-2 col-form-label">Book Style</label>
																												<div class="col-md-4"><select name=book_style  class="form-control form-control-sm">
																																<option value="ALL" {% if query_params.book_style == "ALL" %}selected{% endif %}>All</option>
																																<option value="INTPROC" {% if query_params.book_style == "INTPROC" %}selected{% endif %}>Interproceedings</option>
																																<option value="JOURNAL" {% if query_params.book_style == "JOURNAL" %}selected{% endif %}>Jounals</option>
																																<option value="CONF_DOMESTIC" {% if query_params.book_style == "CONF_DOMESTIC" %}selected{% endif %}>Domestic Conference</option>
																																<option value="CONF_DOMESTIC_NO_REVIEW" {% if query_params.book_style == "CONF_DOMESTIC_NO_REVIEW" %}selected{% endif %}>Domestic Conf(NoReview)</option>
																																<option value="CONF_NATIONAL" {% if query_params.book_style == "CONF_NATIONAL" %}selected{% endif %}>National Conference</option>
																																<option value="BOOK" {% if query_params.book_style == "BOOK" %}selected{% endif %}>Book/Review/Editor</option>
																																<option value="KEYNOTE" {% if query_params.book_style == "KEYNOTE" %}selected{% endif %}>Presentaion/Seminer</option>
																																<option value="NEWS" {% if query_params.book_style == "NEWS" %}selected{% endif %}>New Paper article</option>
																																<option value="OTHERS" {% if query_params.book_style == "OTHERS" %}selected{% endif %}>others</option>
																																<option value="AWARD" {% if query_params.book_style == "AWARD" %}selected{% endif %}>Award</option>
																												</select></div>
																												<label for="example-text-input" class="col-md-2 col-form-label">Sort</label>
																												<div class="col-md-4"><select name=order  class="form-control form-control-sm">
																																<option value="ascending" {% if query_params.order == "ascending" %}selected{% endif %}>Ascending by Date</option>
																																<option value="desending" {% if query_params.order == "desending" %}selected{% endif %}>Desending by Date</option>
																												</select></div>
																								</div>

																								<div class="form-group row">
																												<label for="example-text-input" class="col-md-2 col-form-label">Year</label>
																												<div class="col-md-4">
																																<input type="number" min="1000" max="3000" class="form-control form-control-sm" value="{% if query_params.pubyear %}{{query_params.pubyear}}{% endif %}" aria-label="PubYear" aria-describedby="basic-addon2" name="pubyear">
																																<div class="row">
																																				<div class="form-check">
    																																						<div class="col">

																																												<input class="form-check-input" type="checkbox" id="defaultCheck1" name="pubyear_all" value="checked" {% if query_params.pubyear_all == "checked" %}checked="checked"{% endif %} >
																																												<label class="form-check-label" for="defaultCheck1">
																																																See All
																																												</label>
    																																						</div>
																																				</div>
																																				<div class="form-check">
		    																																				<div class="col">
																																												<input class="form-check-input" type="checkbox" id="defaultCheck2" name="pubyear_type" value="checked" {% if query_params.pubyear_type == "checked" %}checked="checked"{% endif %} >
																																												<label class="form-check-label" for="defaultCheck2">
																																																fiscal year
																																												</label>
																																								</div>
																																				</div>
																																</div>
																												</div>
																								</div>

		    																</form>
																</div>
																<div class="col-12 mb-1">
																				<div class="btn-group btn-group-sm" role="group" aria-label="Basic example">
																								<a href="{% url 'dashboard:index_tile' %}?{% if query_params.keywords %}keywords={{query_params.keywords}}&{% endif %}{% if query_params.book_style %}book_style={{query_params.book_style}}&{% endif %}{% if query_params.order %}order={{query_params.order}}&{% endif %}{% if query_params.pubyear %}pubyear={{query_params.pubyear}}&{% endif %}{% if query_params.pubyear_type %}pubyear_type={{query_params.pubyear_type}}&{% endif %}{% if query_params.pubyear_all %}pubyear_all={{query_params.pubyear_all}}{% endif %}" class="btn btn{% if display_mode != 'tile' %}-outline{% endif %}-secondary" >Tile View</a>
																								<a href="{% url 'dashboard:index_list' %}?{% if query_params.keywords %}keywords={{query_params.keywords}}&{% endif %}{% if query_params.book_style %}book_style={{query_params.book_style}}&{% endif %}{% if query_params.order %}order={{query_params.order}}&{% endif %}{% if query_params.pubyear %}pubyear={{query_params.pubyear}}&{% endif %}{% if query_params.pubyear_type %}pubyear_type={{query_params.pubyear_type}}&{% endif %}{% if query_params.pubyear_all %}pubyear_all={{query_params.pubyear_all}}{% endif %}" class="btn btn{% if display_mode != 'list' %}-outline{% endif %}-secondary" >List View</a>
																								<a href="{% url 'dashboard:index_table' %}?{% if query_params.keywords %}keywords={{query_params.keywords}}&{% endif %}{% if query_params.book_style %}book_style={{query_params.book_style}}&{% endif %}{% if query_params.order %}order={{query_params.order}}&{% endif %}{% if query_params.pubyear %}pubyear={{query_params.pubyear}}&{% endif %}{% if query_params.pubyear_type %}pubyear_type={{query_params.pubyear_type}}&{% endif %}{% if query_params.pubyear_all %}pubyear_all={{query_params.pubyear_all}}{% endif %}" class="btn btn{% if display_mode != 'table' %}-outline{% endif %}-secondary" >Table View</a>
																								<a href="{% url 'dashboard:index_bibtex' %}?{% if query_params.keywords %}keywords={{query_params.keywords}}&{% endif %}{% if query_params.book_style %}book_style={{query_params.book_style}}&{% endif %}{% if query_params.order %}order={{query_params.order}}&{% endif %}{% if query_params.pubyear %}pubyear={{query_params.pubyear}}&{% endif %}{% if query_params.pubyear_type %}pubyear_type={{query_params.pubyear_type}}&{% endif %}{% if query_params.pubyear_all %}pubyear_all={{query_params.pubyear_all}}{% endif %}" class="btn btn{% if display_mode != 'bibtex' %}-outline{% endif %}-secondary" >Bibtex View</a>
																								<a href="{% url 'dashboard:index_latex' %}?{% if query_params.keywords %}keywords={{query_params.keywords}}&{% endif %}{% if query_params.book_style %}book_style={{query_params.book_style}}&{% endif %}{% if query_params.order %}order={{query_params.order}}&{% endif %}{% if query_params.pubyear %}pubyear={{query_params.pubyear}}&{% endif %}{% if query_params.pubyear_type %}pubyear_type={{query_params.pubyear_type}}&{% endif %}{% if query_params.pubyear_all %}pubyear_all={{query_params.pubyear_all}}{% endif %}" class="btn btn{% if display_mode != 'latex' %}-outline{% endif %}-secondary d-none d-md-inline" >Latex View</a>
																				</div>
																</div>
												</div>
								</div>
				</div>
				<div class="card-footer">
								<div style="text-align: right;color:#3C3C3C;font-size: 80%;">{{ query_params.num_hits }} hits</div>
				</div>
</div>
