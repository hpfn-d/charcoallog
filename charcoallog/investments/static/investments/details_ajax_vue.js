var details_ajax = new Vue({
    el: "#vue_ajax_detail",
    methods: {
        submitForm: function(old_money, event) {
            var form = {}
            form["pk"] = Number(event.target.pk.value);
            form['quant'] = Number(event.target.quant.value);
            form["tx_or_price"] = Number(event.target.tx_or_price.value);
            form["segment"] = event.target.segment.value;
            form["which_target"] = event.target.which_target.value;
            form["kind"] = event.target.kind.value;
            form["money"] = Number(event.target.money.value);
            form["date"] = event.target.date.value;

            event.target.checkbox.checked = false
            http_verb = event.target.button.innerText
            http_verb = http_verb == 'delete' ? 'delete' : 'put'

            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios.defaults.xsrfCookieName = "csrftoken";

            axios({
                method: http_verb,
                url: '/investments/details/detail_api/' + form["pk"] + '/',
                data: form
            })
            .then(response => {
                // status code
                if ( http_verb == 'delete') {
                    document.getElementById(form["pk"]).remove()
                }
            })
            .catch(function (err) {
               console.log(err.message);
            })
        }
    }
});
