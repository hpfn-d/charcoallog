Vue.component('line1_accounts_brief', {
    props: ['key_','value_'],
    template:`

        <li class="nav-item nav-link text-muted" id="k_k_" @click="account_call(vl)">

            {{ k_ }}<br>
			<span id="k_" :style="styleObject"> {{ vl }}</span>
			
		</li>
		
	`,
	data: function() {
        return {
            k_: this.key_,
            vl: this.value_,
            display4: false,
            whats_left: parseFloat(document.getElementById("left").textContent)
        }
    },
    computed: {
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
        account_call: function(num) {

            this.whats_left = parseFloat(document.getElementById("left").textContent)
            var num_ = parseFloat(num);

            if (this.display4) {
                document.getElementById("left").textContent = this.whats_left + num_
                this.display4 = false;
            } else {
                document.getElementById("left").textContent = this.whats_left - num_
                this.display4 = true;
            }
        },
    },
});