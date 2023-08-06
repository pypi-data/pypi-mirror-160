import os, re
import fire

def filter_config(output_root, config_list):
  # filter_config_list = []
  para_dic = {}
  for config_tuple in config_list:
    if config_tuple[0] == 'para':
      file, para = config_tuple[1], config_tuple[2]
      value = ''
      if os.path.exists(output_root + file):
        for ln in open(output_root + file):
          if ln.startswith(para):
            try:
              value = ln.split(',')[1].strip()
            except:
              print('no', file)
              continue
      # if value:
        # filter_config_list.append( (para, value) )
      para_dic[para] =value
    else:
      file, para = config_tuple[1], config_tuple[2]
      if os.path.exists(output_root + file):
        # filter_config_list.append( (para , file) )
        para_dic[para] =file
      else:
        para_dic[para] =""
  return para_dic


def parse_config(output_root, config_list):
  para_dic = filter_config(output_root, config_list)
  return para_dic



def render_template(para_dic,  output_root):
  template = open(os.path.split(os.path.realpath(__file__))[0] + '/templates/template.html').read()
  # 模板包括# 样式 style
  os.system( 'cp -r %s %s'%(os.path.split(os.path.realpath(__file__))[0]+'/templates/static/', output_root+'static/'))
  # 输入 output文件夹， 在output文件夹中写入index.html

  f = open(output_root + 'index.html', 'w')
  res = template.replace("data:{'replace':'here'}", 'data: %s'%str(para_dic) )
  # print( res )
  # 循环 show变量字典， 如果 False, 把内容删掉。

  f.write(res)
  f.close()

def dic2str(dic):
  s = '{ '
  for k, v in dic.items():
    if isinstance(v, str):
      s+= k
      s+=': "'
      s+= v
      s+='",'
    if isinstance(v, list):
      s+= k + ': ["' + '","'.join(str(x) for x in v) + '"]'
  s+= ' }'
  return s

def main(output_root='./tmp_output/', type='all'):
  # 思路：
  # 1 html中引入 vue, 从而实现模板, 用变量和 v-if=变量 从而决定渲染
  # 所有参数有个默认值 ''
  # 如果检查成果，这个默认值变成具体值

  # 2 根据type 生成 参数字典
  ## type 可选 'all', 'server', 'accessment', 'quantification', 'pause', 'network'

  # 3 检测参数函数
  ## 用tuple(type, file, key) 表示
  ## a 元素 是否存在，('ele', file, key)
  ## b 文件存在。 ('file', file, key)

  # 4 渲染函数
  ## 把html和statics拷贝进output文件夹，
  ## 修改html的data，把参数字典 导入到vue的data中。

  type_dic = {
    # tuple 1 para或file或img 2 file地址 3 变量名
    'preprocess': [
      ('para', 'csv/preprocess_report.csv', 'Read1_name'),
      ('para', 'csv/preprocess_report.csv', 'Read2_name'),
      ('para', 'csv/preprocess_report.csv', 'Read1_num'),
      ('para', 'csv/preprocess_report.csv', 'Read2_num'),
      ('para', 'csv/preprocess_report.csv', 'Read1_size'),
      ('para', 'csv/preprocess_report.csv', 'Read2_size'),
      ('para', 'csv/preprocess_report.csv', 'Reads_with_adapter'),
      ('para', 'csv/preprocess_report.csv', 'Uninformative_adapter_reads'),
      ('para', 'csv/preprocess_report.csv', 'Pct_uninformative_adapter_reads'),
      ('para', 'csv/preprocess_report.csv', 'Peak_adapter_insertion_size'),
      ('para', 'csv/preprocess_report.csv', 'Adapter_loss_rate'),
      ('para', 'csv/preprocess_report.csv', 'Degradation_ratio'),
      ('para', 'csv/preprocess_report.csv', 'Trimmed_reads'),
      ('para', 'csv/preprocess_report.csv', 'Trim_loss_rate'),
      ('para', 'csv/preprocess_report.csv', 'Reads_with_polyX'),
      ('para', 'csv/preprocess_report.csv', 'Uninformative_polyX_reads'),

      ('para', 'csv/mapping_report.csv', 'assign_mapped'),
      ('para', 'csv/mapping_report.csv', 'NRF'),
      ('para', 'csv/mapping_report.csv', 'PBC1'),
      ('para', 'csv/mapping_report.csv', 'PBC2'),
      ('para', 'csv/mapping_report.csv', 'chrM_mapped'),


      ('file', 'fastq/clean_read1.fq.gz', 'clean_read1'),
      ('file', 'fastq/clean_read2.fq.gz', 'clean_read2'),

      ('file', 'sam/original.sam', 'original_sam'),
      ('file', 'sam/unmapped.sam', 'unmapped_sam'),
      ('file', 'sam/assign.sam', 'assign_sam'),
      ('file', 'sam/unassign.sam', 'unassign_sam'),
      ('file', 'sam/uniquemapped.sam', 'uniquemapped_sam'),
      ('file', 'sam/multimapped.sam', 'multimapped_sam'),
      ('file', 'sam/redundant.sam', 'redundant_sam'),
      ('file', 'sam/nonredundant.sam', 'nonredundant_sam'),

      ('file', 'bw/forward_bw', 'forward_bw'),
      ('file', 'bw/reverse_bw', 'reverse_bw'),
      ('img', 'imgs/adapter_insertion_distribution.png', 'img_adapter_distribution'),
      ('img', 'imgs/reads_distribution.png', 'img_reads_distribution'),
      ('img', 'imgs/reads_ratio.png', 'img_reads_ratio'),
      ('img', 'imgs/mapping_split.png', 'img_mapping_split'),
    ],
    'featureAssign': [
      ('file', 'csv/all_feature_attrs.csv', 'all_feature_attrs_csv'),
      ('file', 'csv/exon_intron_ratio.csv', 'exon_intron_ratio_csv'),
      ('file', 'csv/lincRNA_baseCount.csv', 'lincRNA_baseCount_csv'),
      ('file', 'csv/lincRNA_ei.csv', 'lincRNA_ei_csv'),
      ('file', 'csv/lincRNA_gb_count.csv', 'lincRNA_gb_count_csv'),
      ('file', 'csv/lincRNA_pi.csv', 'lincRNA_pi_csv'),
      ('file', 'csv/lincRNA_pp_count.csv', 'lincRNA_pp_count_csv'),
      ('file', 'csv/lincRNA_rpkm.csv', 'lincRNA_rpkm_csv'),

      ('file', 'csv/protein_coding_baseCount.csv', 'protein_coding_baseCount_csv'),
      ('file', 'csv/protein_coding_ei.csv', 'protein_coding_ei_csv'),
      ('file', 'csv/protein_coding_gb_count.csv', 'protein_coding_gb_count_csv'),
      ('file', 'csv/protein_coding_pi.csv', 'protein_coding_pi_csv'),
      ('file', 'csv/protein_coding_pp_count.csv', 'protein_coding_pp_count_csv'),
      ('file', 'csv/protein_coding_rpkm.csv', 'protein_coding_rpkm_csv'),

      ('img', 'imgs/exon_intron_ratio.png', 'img_exon_intron_ratio'),
      ('img', 'imgs/chr_rpkm.png', 'img_chr_rpkm')
    ],
    'pausing_sites': [
      ('file', 'bed/pausing_sites.bed', 'pausing_sites_bed'),
      ('img', 'imgs/pause_sites.png', 'img_pause_sites')
    ],
    'network': [
      ('img', 'imgs/network_degree.png', 'img_network_degree'),
      ('img', 'imgs/network_motif.png', 'img_network_motif')
    ]
  }

  # 根据流程 找一遍, 每个流程可能有imgs, 输出的文件，report.txt

  type_show_dic = {
    'server': {'show_basic': '', 'show_assess': 'true', 'show_quant': 'true', 'show_pause': 'true', 'show_network': 'true'},
    'all': {'show_basic':'true', 'show_assess': 'true', 'show_quant': 'true', 'show_pause': 'true', 'show_network': 'true'},
    'assessment': {'show_basic':'true', 'show_assess': 'true', 'show_quant': '', 'show_pause': '', 'show_network': ''},
    'quantification': {'show_basic':'', 'show_assess': 'true', 'show_quant': 'true', 'show_pause': 'true', 'show_network': ''},
    'pausing': {'show_basic':'', 'show_assess': '', 'show_quant': '', 'show_pause': 'true', 'show_network': ''},
    'network': {'show_basic':'', 'show_assess': '', 'show_quant': '', 'show_pause': '', 'show_network': 'true'},
  }
  show_dic = type_show_dic[type]


  if not output_root.endswith('/'): output_root = output_root +'/'
  config_list = type_dic['preprocess'] + type_dic['featureAssign'] + type_dic['pausing_sites'] + type_dic['network']
  para_dic = parse_config(output_root, config_list)
  para_dic.update( show_dic )

  # 单独 为 network模块 识别一下 communities
  if para_dic['show_network']:
    community_list = []
    for community_img in os.listdir(output_root +'imgs/'):
      if community_img.startswith('community_'):
        num = int( community_img.split('_')[1].replace('.png', '') )
        community_list.append( num )
    if community_list == []:
      para_dic['community_list'] = ''
    else:
      para_dic['community_list'] = ['community_%s'%str(x) for x in sorted(community_list)]

  para_str = dic2str( para_dic )
  # print(para_str)
  # 定义好参数 给模板的默认值，大多数为None
  render_template(para_str, output_root)


if __name__ == '__main__':
  fire.Fire( main )