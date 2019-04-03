var home_ajax = new Vue({
    el: "#vue_ajax",
    methods: {
        submitForm: function(event) {
            var form = {}
            form["pk"] = Number(event.target.pk.value)
            form["tx_op"] = event.target.tx_op.value;
            form["brokerage"] = event.target.brokerage.value;
            form["kind"] = event.target.kind.value;
            form["money"] = Number(event.target.money.value);
            form["date"] = event.target.date.value;

            //if ( form['kind'].search('transfer') == -1 && kind != '---' ) {
            //    event.target.checkbox.checked = false
            //}

            http_verb = event.target.button.innerText
            http_verb = http_verb == 'delete' ? 'delete' : 'put'

            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios.defaults.xsrfCookieName = "csrftoken";

            axios({
                method: http_verb,
                url: 'home_api/' + form["pk"] + '/',
                data: form
            }).then(response => {
                console.log("HERE")
                if ( http_verb == 'delete') {
                    document.getElementById(form["pk"]).remove()
                }
                // Update line1 data missing
            })
            .catch(function (err) {
                console.log(err.message);
            })
        }
    }
});
