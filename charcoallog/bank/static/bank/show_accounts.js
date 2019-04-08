var bus = new Vue({});


var brief = new Vue({
    el: "#line1_accounts",
    data: {
        out: {},
        whats_left: Number(document.getElementById("left").textContent)
    },
    computed: { // This is not working. There is no 'this.vl'
        styleObject() {
            var font_color = 'black';
            if (this.vl < 0)
                font_color = 'red';
            return {
                color: font_color
            };
        },
    },
    methods: {
        account_call: function(event) {

            this.whats_left = Number(document.getElementById("left").textContent)
            var num_ = Number(event.target.lastChild.innerText)

            var key_ = event.target.id
            var len_key_ = key_.length / 2
            key_ = key_.slice(0,len_key_)

            if (this.out.hasOwnProperty(event.target.id)) {
                document.getElementById("left").textContent = parseFloat(this.whats_left + num_)
                document.getElementById(key_).style.color = 'black'
                delete this.out[event.target.id]

            } else {
                document.getElementById("left").textContent = parseFloat(this.whats_left - num_)
                document.getElementById(key_).style.color = 'purple'
                this.out[event.target.id] = 'inative'

            }
        },
    },
});

// line3 - in Extract db
var bank_ajax = new Vue({
    el: "#vue_ajax",
    methods: {
        submitForm: function(event) {
            var old_payment = event.target.old_payment.value;

            var form = {}
            form["pk"] = Number(event.target.pk.value)
            form["category"] = event.target.category.value;
            form["payment"] = event.target.payment.value;
            form["description"] = event.target.description.value;
            form["money"] = Number(event.target.money.value);
            form["date"] = event.target.date.value;

            //event.target.checkbox.checked = false
            // change button too. After http_verb

            http_verb = event.target.button.innerText
            http_verb = http_verb == 'delete' ? 'delete' : 'put'

            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios.defaults.xsrfCookieName = "csrftoken";

            axios({
                method: http_verb,
                url: 'home_api/' + form["pk"] + '/',
                data: form
            }).then(response => {
                // Check status code!


                if ( http_verb == 'delete' ) {

                    // DRF DELETE returns nothing
                    // math to update line1 data - minor

                    // whats_left_value - form_money
                    var current_whats_left_value = Number(document.getElementById("left").textContent)
                    var left_atual_value = parseFloat(current_whats_left_value - form["money"])
                    document.getElementById("left").textContent = left_atual_value


                    // account_value - form_money
                    var current_account_value = Number(document.getElementById(form["payment"]).textContent)
                    var account_atual_value = parseFloat(current_account_value - form["money"])
                    document.getElementById(form["payment"]).textContent = account_atual_value

                    document.getElementById(form["pk"]).remove()
                }

                if ( http_verb == 'put' ) {

                    if ( old_payment != form['payment']) {
                        document.getElementById(old_payment).textContent = 0;
                        document.getElementById(old_payment+old_payment).remove();
                    }

                    $.each(response.data.accounts, function(index, value) {

                        if ($("[id='"+index+"").length < 1) {
                            // learn Vue
                            // creates a new account
                            var new_account = document.createElement('li');

                            new_account.id = index+index;
                            new_account.className = 'nav-item nav-link text-muted';
                            var text = index + '<br><span id="' + index +'">' + value['money__sum'] + '</span>'
                            new_account.innerHTML = text;
                            var t = document.getElementsByTagName('ul')[1].appendChild(new_account);
                        }
                        ;
                        document.getElementById(index).textContent = value['money__sum']
                    });

                    document.getElementById("left").textContent = response.data.whats_left
                }
            })
            .catch(function (err) {
                console.log(err.message);
            })
        }
    }
})

// line3 - in Schedule
var schedule_ajax = new Vue({
    el: "#vue_schedule_ajax",
    data: {
        display_future: false
    },
    methods: {
        submitForm: function(event) {
            var form = {}
            form["pk"] = Number(event.target.pk.value)
            form["money"] = Number(event.target.money.value);

            // vue 2.6.0
            //event.target.checkbox.checked = false
            // change button too. After http_verb

            http_verb = event.target.button.innerText
            http_verb = http_verb == 'delete' ? 'delete' : 'put'

            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios.defaults.xsrfCookieName = "csrftoken";

            axios({
                method: http_verb,
                url: 'schedule_api/' + form["pk"] + '/',
                data: form
            }).then(response => {
                if ( http_verb == 'delete' && response.status == 204) {
                    var current_whats_left_value = Number(document.getElementById("schedule_whats_left").textContent)
                    var left_atual_value = parseFloat(current_whats_left_value - form["money"])
                    document.getElementById("schedule_whats_left").textContent = left_atual_value

                    document.getElementById(form["pk"]).remove()
                }
                if ( http_verb == 'put' && response.status == 200) {
                    document.getElementById('schedule_whats_left').textContent =response.data.whats_left
                }
            })
            .catch(function (err) {
                console.log(err.message);
            })
        }
    }
})
