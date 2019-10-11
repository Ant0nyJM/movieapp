
function formNotEmpty(form){
  if(form.q.value.length == 0) {
    form.q.placeholder="Enter a search query";
    return false;
  }
  return true;

}