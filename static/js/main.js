function loadAllTickets() {
  $.ajax({
    url: '/api/tickets',
    dataType: 'json'
  }).done(function(data) {
    console.log(data);
    var html = '';
    for (var i = data.length - 1; i >= 0; i--) {
      html += '<div class="col s12">';
      html += '<div class="card blue-grey darken-1">';
      html += '<div class="card-content white-text">';
      html += '<span class="card-title">' + data[i].title + '</span>';
      html += '<p>' + data[i].description + '</p>';
      html += '<ul>';
      html += '<li> Ticket Asignado a:' + data[i].asignee + '</li>';
      html += '<li> Persona que asigna el ticket:' + data[i].reporter + '</li>';
      html += '</ul>';
      html += '<div class="card-action">';
      html += 'Relacionado Con: <a href="/' + data[i].resource_id + '">' + data[i].resource_id + '</a>';
      html += '</div>';
      html += '</div>';
      html += '</div>';
      html += '</div>';
    }
    $("#tickets").html(html);
  });
}

function loadTickets() {
  $.ajax({
    url: '/api/resources' + window.location.pathname + '/tickets',
    dataType: 'json'
  }).done(function(data) {
    console.log(data);
    var html = '';
    if (data.length > 0) {
      html += '<h4>Tickets</h4>';
    }
    for (var i = data.length - 1; i >= 0; i--) {
      html += '<div class="col s12 m6">';
      html += '<div class="card blue-grey darken-1">';
      html += '<div class="card-content white-text">';
      html += '<span class="card-title">' + data[i].title + '</span>';
      html += '<p>' + data[i].description + '</p>';
      html += '<ul>';
      html += '<li> Ticket Asignado a:' + data[i].asignee + '</li>';
      html += '<li> Persona que asigna el ticket:' + data[i].reporter + '</li>';
      html += '</ul>';
      html += '<div class="card-action">';
      html += '<a id="' + data[i].ticket_id + '" href="javascript:void(0);" onclick="deleteTicket(this.id)">Ticket finalizado</a>';
      html += '</div>';
      html += '</div>';
      html += '</div>';
      html += '</div>';
    }
    $("#tickets").html(html);
  });
}

function createTicket() {
  $.ajax({
    type: 'POST',
    url: '/api/resources' + window.location.pathname + '/tickets',
    contentType: 'application/json',
    data: JSON.stringify({
      title: $("#title").val(),
      asignee: $("#asignee").val(),
      reporter: $("#reporter").val(),
      description: $("#description").val()
    })
  }).done(function(data) {
    console.log(data);
    $("#title").val('');
    $("#asignee").val('');
    $("#reporter").val('');
    $("#description").val('');
    Materialize.toast('Se guardó el ticket de manera exitosa', 3000);
    loadTickets();
  }).error(function(data) {
    console.log(data);
    Materialize.toast('No se pudo guardar el ticket', 4000)
  });
}

function deleteTicket(id) {
  $.ajax({
    type: 'DELETE',
    url: '/api/resources' + window.location.pathname + '/tickets/' + id,
    dataType: 'json'
  }).done(function(data) {
    console.log(data);
    loadTickets();
    Materialize.toast('Se borró el ticket de manera exitosa', 3000);
  });
}

function clearResourcesForm() {
  $("#resource_id").val('');
  $("#name").val('');
}

function createResource() {
  $.ajax({
    type: 'POST',
    url: '/api/resources',
    contentType: 'application/json',
    data: JSON.stringify({
      resource_id: $("#resource_id").val(),
      name: $("#name").val()
    })
  }).done(function(data) {
    console.log(data);
    Materialize.toast('Se guardó el dispositivo de manera exitosa', 3000);
    clearResourcesForm();
  }).error(function(data) {
    console.log(data);
    Materialize.toast('No se pudó guardar el dispositivo', 4000)
  });
}

function setUserNamesForAutoComplete() {
  $.ajax({
    type: 'GET',
    url: '/api/users',
    contentType: 'json'
  }).done(function(result) {
    console.log(result);
    $('input.autocomplete').autocomplete({
      data: result
    });
  });
}