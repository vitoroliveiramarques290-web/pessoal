# Workflows RunningHub — imagem/vídeo com modelo de referência + sites

Um workflow completo (00) e cinco workflows separados (01 a 05) em ComfyUI (formato API) feitos só com **nodes nativos do ComfyUI**, para evitar custom nodes que talvez não existam no RunningHub.

| Arquivo | O que faz |
| --- | --- |
| `01_imagem_minha_foto_mais_referencia.api.json` | Sua foto + foto do modelo de referência → imagem nova com **o seu rosto** na pose, roupa, luz e cenário da referência (Qwen-Image-Edit-2509). |
| `02_video_a_partir_de_imagem.api.json` | Uma imagem → vídeo de ~5 s (Wan 2.2 14B I2V, 4 passos). Use com a imagem gerada no 01. |
| `03_video_loop_para_site.api.json` | Uma imagem → vídeo **em loop sem emenda** (primeiro quadro = último) para fundo/hero de site, 1280x720. |
| `04_tudo_em_um_imagem_e_video.api.json` | Os passos 01 + 02 numa execução: foto + referência → imagem → vídeo. Salva as duas saídas. |
| `05_wan22_animate_meu_personagem_no_video_de_referencia.api.json` | **Wan 2.2 Animate**: a sua imagem de personagem faz o movimento e as expressões de um **vídeo de referência** (modo "move"). |

> **Não foram testados no RunningHub.** Foram montados à mão a partir dos templates oficiais do ComfyUI e os links entre nodes e os nomes de todos os campos foram conferidos por script contra o código-fonte do ComfyUI (e do `comfyui_controlnet_aux`, no caso do DWPose), mas não rodei no site. Veja "Se der erro" abaixo.

## ★ Workflow único: `00_COMPLETO_imagem_animate_e_loop_site.api.json`

Tudo em um só grafo (46 nodes), com **3 saídas**:

1. **Imagem** (`15`): sua foto + modelo de referência → imagem com o seu rosto na pose/roupa/cenário da referência.
2. **Vídeo Animate** (`33`): essa imagem faz o movimento e as expressões de um vídeo de referência (Wan 2.2 Animate).
3. **Vídeo loop para site** (`46`): essa imagem vira um vídeo de 1280x720 em loop sem emenda (Wan 2.2 FLF2V).

Campos:
- `4` LoadImage: **sua foto**. `5` LoadImage: **modelo de referência**. `8` prompt da imagem. `13` KSampler da imagem (`seed`, `steps`, `cfg`).
- `23` LoadVideo: **vídeo de movimento** (converta para 16 fps, veja o ffmpeg na seção 05). `27` prompt do Animate. `28` `width`, `height`, `length` (832x480, 77 quadros).
- `40` prompt do loop. `41` `width`, `height`, `length` (1280x720, 81 quadros).

**Escolha o que rodar.** O ComfyUI só executa as saídas ativas. Para economizar tempo e GPU, desative as que não quer com **Ctrl+M** (mute) no node de saída: `33` (Animate) e/ou `46` (loop). Com os dois desativados, só a imagem é gerada, o que é bom para aprovar o rosto antes de gastar GPU com vídeo. Um grafo com tudo ativo carrega 4 modelos grandes em sequência (Qwen, Animate e Wan I2V alto/baixo ruído), então é o mais lento e o que mais pede VRAM.

Vantagem: o vídeo usa a imagem gerada no mesmo run. Desvantagem: se o rosto não ficar bom, os vídeos saem ruins; por isso rode primeiro só a imagem.

## Como usar no RunningHub

1. Em **Workflow**, crie um workflow novo e importe/cole o JSON (formato API). Se o seu fluxo de importação só aceitar o formato de interface, abra o JSON no ComfyUI local, ele converte, e salve de novo.
2. Confira se os **modelos** abaixo existem na lista do RunningHub e, se o nome for diferente, escolha o equivalente em cada node de loader.
3. Troque as imagens nos nodes `LoadImage` e ajuste os prompts.
4. Rode e depois publique como **AI App** se quiser uma tela simples só com os campos de entrada.

### Modelos usados (nomes dos templates oficiais)

- Imagem (01 e 04): `qwen_image_edit_2509_fp8_e4m3fn.safetensors` (UNET), `qwen_2.5_vl_7b_fp8_scaled.safetensors` (CLIP, tipo `qwen_image`), `qwen_image_vae.safetensors`.
- Vídeo (02, 03 e 04): `wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors`, `wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors`, `umt5_xxl_fp8_e4m3fn_scaled.safetensors` (CLIP, tipo `wan`), `wan_2.1_vae.safetensors`, LoRAs `wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors` e `..._low_noise.safetensors`.

## Campos que você edita (ids dos nodes)

Úteis também para a API do RunningHub (`nodeInfoList`: `nodeId`, `fieldName`, `fieldValue`).

**01 — imagem**
- `4` LoadImage → `image`: **sua foto** (rosto bem visível, de frente, boa luz).
- `5` LoadImage → `image`: **modelo de referência** (define pose, roupa, cenário e tamanho da saída).
- `8` TextEncodeQwenImageEditPlus → `prompt` (a "Picture 1" é a sua foto, a "Picture 2" é a referência).
- `13` KSampler → `seed`, `steps` (20), `cfg` (2.5).

**02 — vídeo a partir de imagem**
- `1` LoadImage → `image`.
- `10` CLIPTextEncode → `text` (descreva o movimento).
- `12` WanImageToVideo → `width`, `height` (1280x720 horizontal; 720x1280 vertical), `length` (81 quadros ≈ 5 s a 16 fps).
- `13` KSamplerAdvanced → `noise_seed`.

**03 — loop para site**
- `1` LoadImage → `image` (a imagem do hero).
- `10` → `text` (movimento sutil). `12` WanFirstLastFrameToVideo → `width`, `height`, `length`.

**04 — tudo em um**
- `4`, `5`, `8` como no 01. Vídeo: `24` → `text` (movimento), `26` → `width`, `height`, `length`.
- O vídeo usa a imagem gerada como quadro inicial, então a proporção do vídeo (`26`) pode cortar a imagem se for diferente da referência. Para referência vertical use 720x1280.

## 05 — Wan 2.2 Animate (seu personagem + vídeo de referência)

A imagem do seu personagem (você) assume o **movimento do corpo e as expressões do rosto** do vídeo de referência. O fundo e a roupa vêm da sua imagem, não do vídeo. Para uma cena de site, gere antes a imagem no 01 e use-a aqui.

Modelos: `wan2.2_animate_14B_bf16.safetensors` (carregado em fp8), `clip_vision_h.safetensors`, `lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors` (LoRA, 6 passos, cfg 1), além de `umt5_xxl_fp8_e4m3fn_scaled.safetensors` e `wan_2.1_vae.safetensors`. A pose vem do node `DWPreprocessor` (pacote **comfyui_controlnet_aux**), que usa `yolox_l.onnx` e `dw-ll_ucoco_384_bs5.torchscript.pt`.

Campos:
- `7` LoadImage → `image`: a sua imagem (corpo inteiro ou meio corpo, rosto nítido).
- `8` LoadVideo → `file`: o vídeo de referência (uma pessoa só, bem enquadrada).
- `12` CLIPTextEncode → `text`: prompt curto.
- `14` WanAnimateToVideo → `width`, `height` (832x480 horizontal, 480x832 vertical), `length` (77 quadros ≈ 4,8 s).
- `15` KSampler → `seed`.

**Importante — taxa de quadros:** o Wan gera a 16 fps e os quadros do vídeo de referência são usados em sequência. Converta o vídeo antes de enviar, senão o movimento sai em câmera lenta:

```bash
ffmpeg -i referencia.mp4 -an -r 16 -vf "scale=832:-2" referencia_16fps.mp4
```

Limites desta versão: gera **um trecho** (`length`), sem som, e só no modo "move". A troca de personagem dentro do vídeo original (modo "replace", com o fundo do vídeo) precisa de uma máscara do personagem, feita com SAM2 (custom nodes), que não incluí.

## Dicas de resultado

- **Rosto parecido**: use uma foto sua nítida e de frente; no prompt repita "keep the exact face and identity of Picture 1". Se a identidade escorregar, suba `steps` para 28–30 e `cfg` para 3–4.
- **Referência**: escolha uma foto em que a pessoa esteja inteira/enquadrada como você quer; evite várias pessoas.
- **Vídeo**: movimentos pequenos funcionam melhor ("subtle head turn", "slow camera push-in"). Movimentos grandes deformam o rosto.
- **Loop para site**: no 03, primeiro e último quadro são iguais, então há um quadro repetido na emenda; corte 1 quadro no ffmpeg se notar uma micro-pausa.
- Ideias de prompt de fundo de site: `slow cinematic push-in, soft light rays, floating dust particles`, `gentle parallax, subtle fabric and hair movement`, `abstract gradient light slowly shifting, seamless loop`.

## Preparar o vídeo para o site (ffmpeg)

```bash
ffmpeg -i rh_video.mp4 -an -vf "scale=1280:-2,fps=24" -c:v libx264 -crf 26 -preset slow -pix_fmt yuv420p -movflags +faststart hero.mp4
```

```bash
ffmpeg -i rh_video.mp4 -an -vf "scale=1280:-2" -c:v libvpx-vp9 -crf 34 -b:v 0 hero.webm
```

```bash
ffmpeg -i rh_video.mp4 -frames:v 1 -vf "scale=1280:-2" hero-poster.jpg
```

No HTML:

```html
<video autoplay muted loop playsinline preload="metadata" poster="hero-poster.jpg">
  <source src="hero.webm" type="video/webm" />
  <source src="hero.mp4" type="video/mp4" />
</video>
```

## Se der erro

- **Node não encontrado** (`TextEncodeQwenImageEditPlus`, `WanFirstLastFrameToVideo`, `WanAnimateToVideo`, `CFGNorm`, `ImageScaleToTotalPixels`): a versão do ComfyUI do RunningHub é antiga. Escolha o ambiente/versão mais recente do ComfyUI no workflow.
- **Modelo não encontrado**: troque pelo nome equivalente que o RunningHub oferece no loader; se não houver Qwen-Image-Edit-2509, o equivalente é FLUX.1 Kontext com dois `ReferenceLatent` (posso montar uma versão).
- **Falta de VRAM**: reduza `megapixels` nos nodes `6` e `7` (01) para 0.7 e `width/height` do vídeo para 832x480.

## Fora do escopo

A troca de personagem **dentro de um vídeo existente, mantendo o fundo** (como no app `openjutsu`, que usa MiniMax H3 e SAM 3.1 em GPU local) não está coberta; o 05 só transfere o movimento para a sua imagem.
