export type PublicationType = 'journal' | 'conference' | 'book' | 'patent' | 'thesis'

export interface Publication {
  id: number
  title_uz: string
  title_en: string
  title_ru?: string
  abstract_uz?: string
  abstract_en?: string
  abstract_ru?: string
  authors: string
  journal?: string
  year: number
  volume?: string
  issue?: string
  pages?: string
  doi?: string
  isbn?: string
  url?: string
  pub_type: PublicationType
  language: string
  keywords?: string
  content_uz?: string
  content_en?: string
  content_ru?: string
  pdf_path?: string
  certificate_path?: string
  is_published: boolean
  views: number
  created_at: string
  updated_at: string
}

export interface PublicationList {
  items: Publication[]
  total: number
  page: number
  limit: number
  pages: number
}

export interface Education {
  id: number
  degree: string
  institution: string
  year_start?: number
  year_end?: number
  description?: string
  order: number
}

export interface Experience {
  id: number
  position: string
  organization: string
  year_start?: number
  year_end?: number
  description?: string
  order: number
}

export interface Award {
  id: number
  title: string
  organization?: string
  year?: number
  description?: string
  order: number
}

export interface Profile {
  id: number
  full_name_uz: string
  full_name_en: string
  full_name_ru?: string
  bio_uz?: string
  bio_en?: string
  bio_ru?: string
  avatar_url?: string
  email?: string
  phone?: string
  linkedin?: string
  github?: string
  google_scholar?: string
  orcid?: string
  resume_pdf_path?: string
  position_uz?: string
  position_en?: string
  position_ru?: string
  institution_uz?: string
  institution_en?: string
  institution_ru?: string
  research_interests?: string
  site_title: string
  site_description?: string
  educations: Education[]
  experiences: Experience[]
  awards: Award[]
}
