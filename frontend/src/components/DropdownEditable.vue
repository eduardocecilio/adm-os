<script setup>
import { ref, nextTick, watch } from 'vue'

const props = defineProps({
  modelValue: String,
  opcoes: {
    type: Array,
    default: () => []
  },
  placeholder: {
    type: String,
    default: "Selecione..."
  }
})

const emit = defineEmits(['update:modelValue'])

// Estados
const isEditing = ref(false)
const isCustom = ref(false)
const inputRef = ref(null)

// Monitora alterações
watch(() => props.modelValue, (newVal) => {
  if (isEditing.value) return 

  if (newVal && newVal.trim() !== '' && !props.opcoes.includes(newVal)) {
    isCustom.value = true
  } else {
    isCustom.value = false
  }
}, { immediate: true })

// --- Lógica ---

const onSelectChange = async (event) => {
  const valor = event.target.value
  if (valor === 'Personalizado') {
    isCustom.value = true
    isEditing.value = true
    emit('update:modelValue', '') 
    await nextTick()
    inputRef.value?.focus()
  } else {
    isCustom.value = false
    isEditing.value = false
    emit('update:modelValue', valor)
  }
}

const finalizarEdicao = () => {
  if (!props.modelValue || props.modelValue.trim() === '') {
    isCustom.value = false
    isEditing.value = false
    emit('update:modelValue', '')
  } else {
    isEditing.value = false
  }
}

const editarTexto = async () => {
  isEditing.value = true
  await nextTick()
  inputRef.value?.focus()
}
</script>

<template>
  <div class="dropdown-editable">
    
    <div v-if="isCustom && isEditing" class="custom-wrapper">
      <input 
        ref="inputRef"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        class="input-custom"
        placeholder="Digite o nome..."
        @blur="finalizarEdicao"
        @keydown.enter="finalizarEdicao"
      />
      <span class="icon-edit">✎</span>
    </div>

    <div 
      v-else-if="isCustom && !isEditing" 
      class="custom-wrapper clickable"
      @click="editarTexto"
      title="Clique para editar"
    >
      <div class="fake-select">{{ modelValue }}</div>
      <span class="icon-edit">✎</span>
    </div>

    <select 
      v-else 
      :value="modelValue" 
      @change="onSelectChange" 
      class="select-padrao"
    >
      <option value="" disabled selected>{{ placeholder }}</option>
      <option v-for="op in opcoes" :key="op" :value="op">{{ op }}</option>
      <option value="Personalizado" class="option-bold">➕ Personalizado...</option>
    </select>

  </div>
</template>

<style scoped>
.dropdown-editable { width: 100%; position: relative; }

/* Wrapper para posicionar o ícone do lápis */
.custom-wrapper { position: relative; width: 100%; }
.custom-wrapper.clickable { cursor: pointer; }

/* Estilos Básicos Compartilhados (Tamanho, Fonte, Borda) */
.select-padrao, .input-custom, .fake-select {
  width: 100%;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background-color: white;
  font-size: 0.95rem;
  color: #2d3748;
  box-sizing: border-box;
  height: 42px;
  text-align: left;
  line-height: normal;
  display: block;
}

/* 1. SELECT PADRÃO (Com Seta) */
.select-padrao {
  cursor: pointer;
  appearance: none;
  padding: 10px 35px 10px 10px; /* Espaço na direita para a seta */
  background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%232d3748%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
  background-repeat: no-repeat;
  background-position: right 15px top 50%;
  background-size: 10px auto;
}

/* 2. INPUT CUSTOM (Sem seta, com borda azul ao focar) */
.input-custom {
  padding: 10px 35px 10px 10px; /* Espaço na direita para o lápis */
  border-color: #4299e1;
  outline: none;
  box-shadow: 0 0 0 2px rgba(66, 153, 225, 0.1);
}

/* 3. FAKE SELECT (Sem seta, visual limpo) */
.fake-select {
  padding: 10px 35px 10px 10px; /* Espaço na direita para o lápis */
  cursor: pointer;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  /* IMPORTANTE: Sem background-image aqui, pois usaremos o ícone do lápis */
}
.fake-select:hover {
  background-color: #f7fafc;
  border-color: #cbd5e0;
}

/* ÍCONE DE LÁPIS (Posicionado igual para Input e Fake Select) */
.icon-edit {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #a0aec0;
  font-size: 0.9rem; /* Levemente maior */
  pointer-events: none;
}

.option-bold { font-weight: bold; color: #2b6cb0; }
</style>