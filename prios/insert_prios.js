let prio_ids = [];


function add_prio_id(id){
  prio_ids.push(id);
}

function placeholder_to_value() {
  // console.log(prio_ids);
  let elem;
  for (let i = 0; i < prio_ids.length; i++){
    elem = document.getElementById('prioinp'+prio_ids[i].toString());
    if (elem.value.length === 0) {
        elem.value = elem.placeholder;
    }
  }
    return true;
}
