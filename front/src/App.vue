<template>
  <div>
    <TabView @tab-change="nodeChange($event)">
      <TabPanel header="Node A">
        <div class="card">
          <Toolbar>
            <template #left>
              <Button label="Nós" icon="fas fa-project-diagram" class="p-button-info p-mr-2" @click="showNodes" />
              <Button label="Mempool" icon="fas fa-brain" class="p-button-help p-mr-2" @click="showMempool" />
              <Button label="Minerar" icon="fas fa-wrench" class="p-button-warning p-mr-2" @click="mine" />
              <Button label="Resolver" icon="fas fa-balance-scale" class="p-button-danger" @click="resolve" />
            </template>
          </Toolbar>

          <h1>Chain do Node {{currentNodeName}}</h1>
          <Timeline :value="chain">
            <template #marker="slotProps">
              <span class="custom-marker p-shadow-2" >
                <Button icon="fas fa-link" :label="`#${slotProps.item.block.index}`" class="p-button-rounded p-button-warn" @click="showBlock(slotProps.item)"/>
              </span>
            </template>
            <template #content="slotProps">
              {{slotProps.item.id}}
            </template>
          </Timeline>
        </div>        
        </TabPanel>
        <TabPanel header="Node B">
          <div class="card">
          <Toolbar>
            <template #left>
              <Button label="Nós" icon="fas fa-project-diagram" class="p-button-info p-mr-2" @click="showNodes" />
              <Button label="Mempool" icon="fas fa-brain" class="p-button-help p-mr-2" @click="showMempool" />
              <Button label="Minerar" icon="fas fa-wrench" class="p-button-warning p-mr-2" @click="mine" />
              <Button label="Resolver" icon="fas fa-balance-scale" class="p-button-danger" @click="resolve" />
            </template>
          </Toolbar>

            <h1>Chain do Node {{currentNodeName}}</h1>
            <Timeline :value="chain">
              <template #marker="slotProps">
                <span class="custom-marker p-shadow-2" >
                  <Button icon="fas fa-link" :label="`#${slotProps.item.block.index}`" class="p-button-rounded p-button-warn" @click="showBlock(slotProps.item)"/>
                </span>
              </template>
              <template #content="slotProps">
                {{slotProps.item.id}}
              </template>
            </Timeline>
          </div>        
          </TabPanel>
        </TabView>

    </div>
  <Dialog  v-model:visible="blockVisibility" :style="{width: '50vw'}" :modal="true">
    <template #header> 
      
      <h4>Block #{{this.block.block.index}} {{this.block.id}}</h4>
    </template>
    <div class="p-grid p-mt-4">
      <div class="p-col-2">
        <span class="p-float-label">
          <InputText disabled style="width: 100%" v-model="block.block.index"/>
          <label for="">Index</label>
        </span>
      </div>
      <div class="p-col">
        <span class="p-float-label">
          <InputText disabled style="width: 100%" v-model="block.block.timestamp"/>
          <label for="">Timestamp</label>
        </span>
      </div>
      <div class="p-col">
        <span class="p-float-label">
          <InputText disabled style="width: 100%" v-model="block.block.nonce"/>
          <label for="">Nonce</label>
        </span>
      </div>
    </div>
    <div class="p-grid p-mt-4">
      <div class="p-col">
        <span class="p-float-label">
          <InputText disabled style="width: 100%" v-model="block.block.merkleRoot"/>
          <label for="">Merkle Root</label>
        </span>
      </div>
    </div>
    <div class="p-grid">
      <div class="p-col">
        <Fieldset legend="Transações" :toggleable="true">
          <Card v-for="transaction in block.block.transactions" :key="transaction">
            <template #header>
              Transação #{{block.block.transactions.indexOf(transaction)}}
            </template>
            <template #content>
                <b>Sender:</b> {{transaction.sender}}<br>
                <b>Recipient:</b> {{transaction.recipient}}<br>
                <b>Amount:</b> {{transaction.amount}}<br>
                <b>Timestamp:</b> {{transaction.timestamp}}<br>
                <b>Signature:</b> {{transaction.signature}}<br>
            </template>
          </Card>
        </Fieldset>
      </div>
    </div>
    <template #footer>
        Hash do anterior: {{this.block.block.previousHash}}
    </template>
  </Dialog>
    <Dialog header="Nós registrados" v-model:visible="nodesVisibility" :style="{width: '50vw'}" :modal="true">
    <ul id="example-1">
      <li v-for="node in nodes" :key="node">
        {{ node }}
      </li>
    </ul>

    <template #footer>
      <Button label="Registrar" icon="fas fa-plus" @click="newNodeVisibility=true;"/>
    </template>
  </Dialog>
  <Dialog header="Adicionar node" v-model:visible="newNodeVisibility" :style="{width: '20vw'}" :position="'top'" :modal="true">
    <div class="p-mt-4">
      <span class="p-float-label">
        <InputText style="width: 100%" v-model="newNodeURL"/>
        <label for="">URL</label>
      </span>
    </div>

    <template #footer>
        <Button label="Adicionar" icon="fas fa-plus-square" @click="addNode"/>
    </template>
</Dialog>
<Dialog header="Nós registrados" v-model:visible="nodesVisibility" :style="{width: '50vw'}" :modal="true">
    <ul id="example-1">
      <li v-for="node in nodes" :key="node">
        {{ node }}
      </li>
    </ul>

    <template #footer>
      <Button label="Registrar" icon="fas fa-plus" @click="newNodeVisibility=true;"/>
    </template>
  </Dialog>
  <Dialog header="Mempool" v-model:visible="mempoolVisibility" :style="{width: '70vw'}" :position="'center'" :modal="true">
      <Card v-for="transaction in mempool" :key="transaction">
          <template #header>
            Transação #{{mempool.indexOf(transaction)}}
          </template>
          <template #content>
              <b>Sender:</b> {{transaction.sender}}<br>
              <b>Recipient:</b> {{transaction.recipient}}<br>
              <b>Amount:</b> {{transaction.amount}}<br>
              <b>Timestamp:</b> {{transaction.timestamp}}<br>
              <b>Signature:</b> {{transaction.signature}}<br>
          </template>
      </Card>

    <template #footer>
        <Button label="Transação" class="p-button-success" icon="fas fa-plus" @click="showNewTransaction"/>
    </template>
</Dialog>
<Dialog header="Adicionar Transação" v-model:visible="newTransactionVisibility" :style="{width: '40vw'}" :position="'top'" :modal="true">
    <div class="p-grid p-mt-4">
      <div class="p-col">
        <span class="p-float-label">
          <InputText style="width: 100%" v-model="newTransactionData.sender"/>
          <label for="">Sender</label>
        </span>
      </div>
      <div class="p-col">
        <span class="p-float-label">
          <InputText style="width: 100%" v-model="newTransactionData.recipient"/>
          <label for="">Recipient</label>
        </span>
      </div>
    </div>
    <div class="p-grid p-mt-4">
      <div class="p-col">
        <span class="p-float-label">
          <InputText style="width: 100%" v-model="newTransactionData.amount"/>
          <label for="">Amount</label>
        </span>
      </div>
      <div class="p-col-8">
        <span class="p-float-label">
          <InputText style="width: 100%" v-model="newTransactionData.privWifKey"/>
          <label for="">Key</label>
        </span>
      </div>
    </div>
      

    <template #footer>
        <Button label="Adicionar" icon="fas fa-plus-square" @click="addNewTransaction"/>
    </template>
</Dialog>
<Toast/>
</template>




<script>

export default {
  name: "App",
  components: {},
  data() {
    return {
      chain: null,
      nodes: null,
      block: null,
      newTransactionData: {},
      blockVisibility: false,
      nodesVisibility: false,
      newNodeVisibility: false,
      mempoolVisibility: false,
      newTransactionVisibility: false,
      newNodeURL: null,
      currentNode:0,
      currentNodeName: 'A',
      mempool: null
    };
  },
  mounted() {
    this.axios.get("http://localhost:5000/chain").then((response) => {
      this.chain = response.data;
      this.chain.reverse();
    });
    this.axios.get("http://localhost:5000/node/list").then((response) => {
      this.nodes = response.data;
    });
    this.axios.get("http://localhost:5000/transactions/mempool").then((response) => {
      this.mempool = response.data;
    });
  },
  methods: {
    showBlock(block){
      this.block = block;
      this.blockVisibility=true;
    },
    showNodes(){
      this.nodesVisibility=true;
    },
    showMempool(){
      this.mempoolVisibility=true;
    },
    showNewTransaction(){
      this.newTransactionVisibility=true;
    },
    addNode(){
      this.axios.post(`http://localhost:500${this.currentNode}/node/register`,{node_address:this.newNodeURL}).then((response) => {
        this.nodes = response.data;
      })
    },
    addNewTransaction(){

      this.axios.post(`http://localhost:500${this.currentNode}/transactions/create`,this.newTransactionData).then((response)=>{
        this.mempool = response.data;
        this.newTransactionData = {};
      })
    },
    mine(){
      this.$toast.add({severity:'success',summary:'Minerando bloco!', detail:"Minerando um bloco com as transações da mempool!",life:5000})
      this.axios.get(`http://localhost:500${this.currentNode}/mine`).then((response)=>{
        this.$toast.removeAllGroups()
        this.$toast.add({severity:'success',summary:'Bloco minerado adicionado!', detail:`O bloco foi minerado e a chain foi atualizada! (Nonce: ${response.data.nonce})`,life:5000})
        this.axios.get(`http://localhost:500${this.currentNode}/chain`).then((response) => {
          this.chain = response.data;
          this.chain.reverse();
        });
      })
    },
    resolve(){
      this.axios.get(`http://localhost:500${this.currentNode}/node/resolve`).then((response)=>{
        if (response.data.changed){
          this.axios.get(`http://localhost:500${this.currentNode}/chain`).then((response) => {
            this.chain = response.data;
            this.chain.reverse();
            this.$toast.add({severity:'success',summary:'Chain recuperada!', detail:"Recuperada a blockchain do nó selecionado"})
          });
          this.$toast.add({severity:'success',summary:'Chain substituida!', detail:"Foi feita verificação e a chain do nó foi substituida por uma maior!",life:5000})
        }
        else{
          this.$toast.add({severity:'success',summary:'Chain mantida!', detail:"A chain continua a mesma!",life:3000})
        }
      })
    },
    nodeChange(event){
      // this.$toast.removeGroup('nodeLoad')
      this.currentNode = event.index;
      this.currentNodeName = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[this.currentNode];
      this.axios.get(`http://localhost:500${this.currentNode}/chain`).then((response) => {
        this.chain = response.data;
        this.chain.reverse();
        this.$toast.add({severity:'success',summary:'Chain recuperada!', detail:"Recuperada a blockchain do nó selecionado",life:3000})
      });
      this.axios.get(`http://localhost:500${this.currentNode}/node/list`).then((response) => {
        this.nodes = response.data;
        this.$toast.add({severity:'success',summary:'Nodes recuperados!', detail:"Recuperados os demais nós registrados do nó selecionado",life:3000})
      });
      this.axios.get(`http://localhost:500${this.currentNode}/transactions/mempool`).then((response) => {
        this.mempool = response.data;
        this.$toast.add({severity:'success',summary:'Mempool recuperada!', detail:"Recuperada a mempool do nó selecionado",life:3000})
      });
    }
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
body{
  width: 100vw;
  height: 100vh;
  background-color: var(--surface-b);
}
</style>
