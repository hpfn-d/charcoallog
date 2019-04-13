Vue.component('all-reg-forms', {
    props: ['color', 'pk', 'date', 'money', 'description', 'category', 'payment'],
    template:`
            <div class="form-inline m-0 p-0">
                <input type="hidden" id="pk" name="pk" :value="pk">

                <div @input="n_dt">
                <input type="date" id="date" class="form-inline m-0 p-0 bg-light"
                       :class="{ 'text-muted': isNaN(money)}"
                       size="11" style="font-size:10px;border:none"
                       :value="dt" :disabled="edit"
                       required>
                </div>

                <div @input="n_mn">
                <input type="text" id="money" name="money" step="0.01" class="form-inline m-0 p-0 bg-light"
                       :class="{ 'text-muted': isNaN(money)}"
                       size="11" style="font-size:10px;border:none"
                       :style="styleObject"
                       :value="mn" :disabled="edit"
                       required>
                </div>

                <div @input="n_description">
                <input type="text"  id="description" name="description" class="form-inline m-0 p-0 bg-light"
                       :class="{ 'text-muted': isNaN(money)}"
                       size="20" style="font-size:10px;border:none"
                       :value="dscrptn" :disabled="edit"
                       required>
                </div>

                <div @input="n_category">
                <input type="text"  id="category" name="category" class="form-inline m-0 p-0 bg-light"
                       :class="{ 'text-muted': isNaN(money)}"
                       size="20" style="font-size:10px;border:none"
                       :value="ctgr" :disabled="edit"
                       required>
                </div>

                <div @input="n_payment">
                <input type="text" id="payment" name="payment" class="form-inline m-0 p-0 bg-light"
                       :class="{ 'text-muted': isNaN(money)}"
                       size="20" style="font-size:10px;border:none"
                       :value="pmnt" :disabled="edit"
                       required>
                <input type="hidden" :value=this.payment name="old_payment">
                </div>

                <div class="form-inline m-0 p-0 bg-light" v-if="!isNaN(mn)">
                <input type="checkbox" id="checkbox" v-model:value="chk" v-bind="label()">
                <span class="form-text text-muted" style="font-size:9px">update</span>
                </div>

                <div class="form-inline m-0 p-0" v-if="!isNaN(mn)">
                <button type="submit" class="btn btn-sm m-0 p-0 btn-link" id="button" size="6" @click="dflt()">{{ method }}</button>
                </div>
            </div>
    `,
    data: function() {
        return {
            method: 'delete',
            edit: true,
            chk: false,
            pmnt: this.payment,
            ctgr: this.category,
            dscrptn: this.description,
            mn: this.money,
            dt: this.date,
            //color: this.color
        }
    },
    computed: {
        styleObject() {
            var font_color = 'black';
            if (this.mn < 0)
                font_color = 'red';
            return {
                color: this.color ? this.color : font_color
            };
        },
    },
    methods:{
        n_category: function(event) {
            this.ctgr = event.target.value
        },
        n_payment: function(event) {
            this.pmnt = event.target.value
        },
        n_description: function(event) {
             this.dscrptn = event.target.value
        },
        n_mn: function(event) {
             this.mn = event.target.value
        },
        n_dt: function(event) {
            this.dt = event.target.value
        },
        dflt: function() { // this will change for Vue 2.6.0 - rm
            this.chk = false
        },
        label: function(){
             this.method = this.chk ? 'update' : 'delete';
             this.edit = this.chk == false ? true : false
        },
    },
});
