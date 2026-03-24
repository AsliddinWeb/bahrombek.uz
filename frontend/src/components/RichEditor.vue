<template>
  <div class="rich-editor border border-slate-200 dark:border-slate-700 rounded-xl overflow-hidden">
    <!-- Toolbar -->
    <div class="toolbar flex flex-wrap items-center gap-0.5 px-2 py-1.5 bg-slate-50 dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700">

      <!-- History -->
      <ToolBtn @click="editor?.chain().focus().undo().run()" title="Undo" :disabled="!editor?.can().undo()">
        <PhArrowCounterClockwise :size="15" />
      </ToolBtn>
      <ToolBtn @click="editor?.chain().focus().redo().run()" title="Redo" :disabled="!editor?.can().redo()">
        <PhArrowClockwise :size="15" />
      </ToolBtn>

      <Sep />

      <!-- Headings -->
      <ToolBtn
        v-for="n in [1,2,3]" :key="n"
        @click="editor?.chain().focus().toggleHeading({ level: n as any }).run()"
        :active="editor?.isActive('heading', { level: n })"
        :title="`Heading ${n}`"
      >
        <span class="font-bold text-xs">H{{ n }}</span>
      </ToolBtn>

      <ToolBtn
        @click="editor?.chain().focus().setParagraph().run()"
        :active="editor?.isActive('paragraph')"
        title="Paragraph"
      >
        <PhTextT :size="15" />
      </ToolBtn>

      <Sep />

      <!-- Inline -->
      <ToolBtn @click="editor?.chain().focus().toggleBold().run()" :active="editor?.isActive('bold')" title="Bold">
        <PhTextB :size="15" />
      </ToolBtn>
      <ToolBtn @click="editor?.chain().focus().toggleItalic().run()" :active="editor?.isActive('italic')" title="Italic">
        <PhTextItalic :size="15" />
      </ToolBtn>
      <ToolBtn @click="editor?.chain().focus().toggleUnderline().run()" :active="editor?.isActive('underline')" title="Underline">
        <PhTextUnderline :size="15" />
      </ToolBtn>
      <ToolBtn @click="editor?.chain().focus().toggleStrike().run()" :active="editor?.isActive('strike')" title="Strikethrough">
        <PhTextStrikethrough :size="15" />
      </ToolBtn>
      <ToolBtn @click="editor?.chain().focus().toggleHighlight().run()" :active="editor?.isActive('highlight')" title="Highlight">
        <PhHighlighter :size="15" />
      </ToolBtn>
      <ToolBtn @click="editor?.chain().focus().toggleCode().run()" :active="editor?.isActive('code')" title="Inline code">
        <PhCode :size="15" />
      </ToolBtn>

      <Sep />

      <!-- Superscript / Subscript -->
      <ToolBtn @click="editor?.chain().focus().toggleSuperscript().run()" :active="editor?.isActive('superscript')" title="Superscript">
        <PhTextSuperscript :size="15" />
      </ToolBtn>
      <ToolBtn @click="editor?.chain().focus().toggleSubscript().run()" :active="editor?.isActive('subscript')" title="Subscript">
        <PhTextSubscript :size="15" />
      </ToolBtn>

      <Sep />

      <!-- Lists -->
      <ToolBtn @click="editor?.chain().focus().toggleBulletList().run()" :active="editor?.isActive('bulletList')" title="Bullet list">
        <PhListBullets :size="15" />
      </ToolBtn>
      <ToolBtn @click="editor?.chain().focus().toggleOrderedList().run()" :active="editor?.isActive('orderedList')" title="Ordered list">
        <PhListNumbers :size="15" />
      </ToolBtn>
      <ToolBtn @click="editor?.chain().focus().toggleBlockquote().run()" :active="editor?.isActive('blockquote')" title="Blockquote">
        <PhQuotes :size="15" />
      </ToolBtn>
      <ToolBtn @click="editor?.chain().focus().toggleCodeBlock().run()" :active="editor?.isActive('codeBlock')" title="Code block">
        <PhCodeBlock :size="15" />
      </ToolBtn>

      <Sep />

      <!-- Align -->
      <ToolBtn @click="editor?.chain().focus().setTextAlign('left').run()" :active="editor?.isActive({ textAlign: 'left' })" title="Align left">
        <PhTextAlignLeft :size="15" />
      </ToolBtn>
      <ToolBtn @click="editor?.chain().focus().setTextAlign('center').run()" :active="editor?.isActive({ textAlign: 'center' })" title="Align center">
        <PhTextAlignCenter :size="15" />
      </ToolBtn>
      <ToolBtn @click="editor?.chain().focus().setTextAlign('right').run()" :active="editor?.isActive({ textAlign: 'right' })" title="Align right">
        <PhTextAlignRight :size="15" />
      </ToolBtn>
      <ToolBtn @click="editor?.chain().focus().setTextAlign('justify').run()" :active="editor?.isActive({ textAlign: 'justify' })" title="Justify">
        <PhTextAlignJustify :size="15" />
      </ToolBtn>

      <Sep />

      <!-- Link -->
      <ToolBtn @click="setLink" :active="editor?.isActive('link')" title="Link">
        <PhLink :size="15" />
      </ToolBtn>
      <ToolBtn v-if="editor?.isActive('link')" @click="editor?.chain().focus().unsetLink().run()" title="Remove link">
        <PhLinkBreak :size="15" />
      </ToolBtn>

      <!-- Image -->
      <ToolBtn @click="insertImage" title="Image URL">
        <PhImage :size="15" />
      </ToolBtn>

      <Sep />

      <!-- HR -->
      <ToolBtn @click="editor?.chain().focus().setHorizontalRule().run()" title="Horizontal rule">
        <PhMinus :size="15" />
      </ToolBtn>

      <!-- Clear -->
      <ToolBtn @click="editor?.chain().focus().clearNodes().unsetAllMarks().run()" title="Clear formatting">
        <PhTextHFive :size="15" />
      </ToolBtn>
    </div>

    <!-- Editor area -->
    <EditorContent
      :editor="editor"
      class="prose-area min-h-[300px] max-h-[600px] overflow-y-auto"
    />
  </div>
</template>

<script setup lang="ts">
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Underline from '@tiptap/extension-underline'
import Link from '@tiptap/extension-link'
import TextAlign from '@tiptap/extension-text-align'
import Placeholder from '@tiptap/extension-placeholder'
import Image from '@tiptap/extension-image'
import Subscript from '@tiptap/extension-subscript'
import Superscript from '@tiptap/extension-superscript'
import Highlight from '@tiptap/extension-highlight'
import TextStyle from '@tiptap/extension-text-style'
import {
  PhArrowCounterClockwise, PhArrowClockwise, PhTextT, PhTextB, PhTextItalic,
  PhTextUnderline, PhTextStrikethrough, PhHighlighter, PhCode, PhCodeBlock,
  PhTextSuperscript, PhTextSubscript, PhListBullets, PhListNumbers, PhQuotes,
  PhTextAlignLeft, PhTextAlignCenter, PhTextAlignRight, PhTextAlignJustify,
  PhLink, PhLinkBreak, PhImage, PhMinus, PhTextHFive
} from '@phosphor-icons/vue'
import { defineComponent, h, watch } from 'vue'

const props = defineProps<{ modelValue: string; placeholder?: string }>()
const emit = defineEmits<{ 'update:modelValue': [string] }>()

// Inline helper components
const ToolBtn = defineComponent({
  props: { active: Boolean, disabled: Boolean, title: String },
  emits: ['click'],
  setup(props, { slots, emit }) {
    return () => h('button', {
      type: 'button',
      title: props.title,
      disabled: props.disabled,
      onClick: () => emit('click'),
      class: [
        'p-1.5 rounded-lg transition-colors text-slate-600 dark:text-slate-400',
        props.active
          ? 'bg-brand-100 dark:bg-brand-900/40 text-brand-700 dark:text-brand-300'
          : 'hover:bg-slate-200 dark:hover:bg-slate-700',
        props.disabled ? 'opacity-30 cursor-not-allowed' : '',
      ].join(' '),
    }, slots.default?.())
  },
})

const Sep = defineComponent({
  setup: () => () => h('div', { class: 'w-px h-5 bg-slate-200 dark:bg-slate-700 mx-0.5' })
})

const editor = useEditor({
  content: props.modelValue,
  extensions: [
    StarterKit,
    Underline,
    Subscript,
    Superscript,
    Highlight,
    TextStyle,
    TextAlign.configure({ types: ['heading', 'paragraph'] }),
    Link.configure({ openOnClick: false }),
    Image,
    Placeholder.configure({ placeholder: props.placeholder ?? 'Matn yozing...' }),
  ],
  editorProps: {
    attributes: {
      class: 'tiptap-content focus:outline-none px-5 py-4',
    },
  },
  onUpdate({ editor }) {
    emit('update:modelValue', editor.getHTML())
  },
})

watch(() => props.modelValue, (val) => {
  if (editor.value && editor.value.getHTML() !== val) {
    editor.value.commands.setContent(val || '', false)
  }
})

function setLink() {
  const prev = editor.value?.getAttributes('link').href ?? ''
  const url = prompt('URL:', prev)
  if (url === null) return
  if (!url) {
    editor.value?.chain().focus().unsetLink().run()
    return
  }
  editor.value?.chain().focus().setLink({ href: url, target: '_blank' }).run()
}

function insertImage() {
  const url = prompt('Rasm URL:')
  if (url) editor.value?.chain().focus().setImage({ src: url }).run()
}
</script>

<style>
.tiptap-content {
  min-height: 300px;
}

.tiptap-content > * + * { margin-top: 0.75em; }

.tiptap-content h1 { font-size: 1.75rem; font-weight: 700; font-family: 'Playfair Display', serif; }
.tiptap-content h2 { font-size: 1.4rem; font-weight: 700; }
.tiptap-content h3 { font-size: 1.15rem; font-weight: 600; }

.tiptap-content p { line-height: 1.75; }

.tiptap-content strong { font-weight: 700; }
.tiptap-content em { font-style: italic; }
.tiptap-content u { text-decoration: underline; }
.tiptap-content s { text-decoration: line-through; }
.tiptap-content mark { background: #fef08a; padding: 0 2px; border-radius: 2px; }
.dark .tiptap-content mark { background: #713f12; color: #fef9c3; }

.tiptap-content code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875em;
  background: #f1f5f9;
  padding: 0.15em 0.4em;
  border-radius: 4px;
}
.dark .tiptap-content code { background: #1e293b; }

.tiptap-content pre {
  background: #0f172a;
  color: #e2e8f0;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875em;
  padding: 1rem;
  border-radius: 0.75rem;
  overflow-x: auto;
}
.tiptap-content pre code { background: transparent; padding: 0; }

.tiptap-content blockquote {
  border-left: 3px solid #818cf8;
  padding-left: 1rem;
  color: #64748b;
  font-style: italic;
}
.dark .tiptap-content blockquote { color: #94a3b8; }

.tiptap-content ul { list-style: disc; padding-left: 1.5rem; }
.tiptap-content ol { list-style: decimal; padding-left: 1.5rem; }
.tiptap-content li { line-height: 1.75; }

.tiptap-content hr { border-color: #e2e8f0; margin: 1.5rem 0; }
.dark .tiptap-content hr { border-color: #334155; }

.tiptap-content a { color: #4f46e5; text-decoration: underline; }
.dark .tiptap-content a { color: #818cf8; }

.tiptap-content img { max-width: 100%; border-radius: 0.5rem; }

.tiptap-content sup { vertical-align: super; font-size: 0.75em; }
.tiptap-content sub { vertical-align: sub; font-size: 0.75em; }

/* Placeholder */
.tiptap-content p.is-editor-empty:first-child::before {
  content: attr(data-placeholder);
  float: left;
  color: #94a3b8;
  pointer-events: none;
  height: 0;
}
</style>
