module Gem
  class << self
    def root_user_dir
      File.join ['/', 'usr', 'local', 'gems']
    end

    def root_bindir
      File.join ['/', 'usr', 'local', 'bin']
    end

    def rpm_gem_dir
      File.join [ConfigMap[:datadir], 'rubygems', 'gems']
    end

    def default_dir
      if Process.uid == 0
        Gem.root_user_dir
      else
        Gem.user_dir
      end
    end

    def default_path
      path = []
      path << Gem.user_dir if File.exist? Gem.user_home
      path << Gem.root_user_dir
      path << Gem.rpm_gem_dir
    end

    def default_bindir
      if Process.uid == 0
        File.join ['/', 'usr', 'local', 'bin']
      else
        File.join [File.expand_path('~'), 'bin']
      end
    end
  end
end
